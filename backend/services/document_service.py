import os
import logging
from utils.openai__utils import openai_search
from utils.document_utils import doc_s2_build
from doc_generation.template_dic import template_merged
import pandas as pd
import uuid
import re
import time
import json
import markdown
from bs4 import BeautifulSoup
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient  
from azure.search.documents.indexes.models import (  
    SearchIndex,
    SimpleField,
    SearchField,
    VectorSearch,
    VectorSearchProfile,
    SearchFieldDataType,
    CorsOptions,
    SemanticField,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    HnswAlgorithmConfiguration,
    SemanticSearch
)  
from langchain_openai import AzureOpenAIEmbeddings
from services.context_retrieval_service import ContextRetrievalService
from azure.search.documents.models import VectorizedQuery

logging.basicConfig(level=logging.INFO)

async def process_mop(file_path: str, websocket_id: str, manager):  
    try:
        output_dir = "temporalOutput"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        start_document_intelligence_process(file_path, output_dir)
        logging.info("Data preparation script completed.")
            
        sections_dic = {key: "" for key in template_merged}
        total_sections = remaining_sections = len(sections_dic)
        completed_sections = 0
        context_retrieval_service = ContextRetrievalService()
        start_time = time.time()
        logging.info("Document generation script started.")
       
        for section_title in sections_dic.keys():
           
            logging.info(f'Remaining sections: {remaining_sections}')
            
            sections_dic[section_title] = await section_builder(section_title, context_retrieval_service)
        
            remaining_sections -= 1
            completed_sections += 1
            
            progress = (completed_sections / total_sections) * 100
            await manager.send_progress(websocket_id, progress)

        end_time = time.time()     

        with open('log.txt', 'a') as f:
            f.write(f'Time taken: {end_time - start_time} seconds\n')

        generated_document_path = doc_s2_build(sections_dic)
        
        logging.info("Document generation script completed.")

        return generated_document_path
    except Exception as e:
        logging.error(f"Error in process_mop: {e}")
        raise 

    
def start_document_intelligence_process(file_path, output_path, sleep_time_between_request=2):
    logging.info("Starting the document intelligence process...")

    load_dotenv()

    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")  
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")  

    logging.info("Initializing the Document Intelligence client...")
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    try:
        output_file_path = process_file(file_path, document_intelligence_client, output_path, sleep_time=sleep_time_between_request)
    except HttpResponseError as error:
        if error.error is not None:
            logging.info(f"Error code: {error.error.code}, Message: {error.error.message}")
        else:
            logging.info(f"HttpResponseError occurred: {error.message}")
    
    logging.info("Document intelligence process completed")
    md_text=""
    with open(output_file_path, 'r',encoding='utf-8') as file:
        md_text = file.read() 
    sections = parse_markdown(md_text)
    
    df = pd.DataFrame(sections) 
    df.insert(0, 'id', [str(uuid.uuid4()) for _ in range(len(df))]) 
    doc_filename = os.path.basename(file_path)
    df.insert(1, 'doc_name', doc_filename)

    normalize_df(df) 
    df['text_content']= df["text_content"].apply(lambda x : normalize_text(x)) #text is normalized extracting \n and special characters check later as we might use \n\n to delimit tables
    df['combined'] = df['h1'] + '\n' + df['h2'] + '\n' + df['h3'] +'\n'+df['text_content']
    df['vector'] = df['combined'].apply(lambda text: generate_embeddings(text))
    

    key = os.getenv("AZURE_SEARCH_API_KEY")
    endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    credential = AzureKeyCredential(os.environ["AZURE_SEARCH_ADMIN_KEY"]) if len(os.environ["AZURE_SEARCH_ADMIN_KEY"]) > 0 else DefaultAzureCredential()
    search_index_client = SearchIndexClient(endpoint, credential)
    service_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")

    index_name = os.environ['AZURE_SEARCH_INDEX']
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchField(name="doc_name", type=SearchFieldDataType.String),
        SearchField(name="h1", type=SearchFieldDataType.String),
        SearchField(name="h2", type=SearchFieldDataType.String),
        SearchField(name="h3", type=SearchFieldDataType.String),
        SearchField(name="text_content", type=SearchFieldDataType.String),
        SearchField(
            name="vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="my-vector-config"
        )    
    ]

    cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
    vector_search_config = VectorSearch(
        profiles=[VectorSearchProfile(name="my-vector-config", algorithm_configuration_name="my-algorithms-config")],
        algorithms=[
            HnswAlgorithmConfiguration(
                name="my-algorithms-config",
                kind="hnsw",
                parameters={
                    "m": 4,
                    "efConstruction": 400,
                    "efSearch": 500,
                    "metric": "cosine"
                }
            )
        ]
    )

    semantic_config = SemanticConfiguration(
        name="my-semantic-config",
        prioritized_fields=SemanticPrioritizedFields(
            keywords_fields=[
                SemanticField(field_name="doc_name"),       
                SemanticField(field_name="h1"),       
                SemanticField(field_name="h2"),       
                SemanticField(field_name="h3"),       
            ],
            content_fields=  [
                SemanticField(field_name="text_content")
            ],
        )
    )
    semantic_search = SemanticSearch(configurations=[semantic_config])

    delete_index(search_index_client,index_name)

    index_name: str =index_name
    index = SearchIndex(name = index_name,
                        fields = fields,
                        vector_search = vector_search_config,
                        semantic_search = semantic_search,
                        cors_options = cors_options)

    result = search_index_client.create_or_update_index(index)
    logging.info(f'{result.name} index created')


    columns_to_select = [
        "id",  
        "doc_name",    
        "h1",
        "h2",
        "h3",
        "text_content",
        "vector"
    ]

    #df.to_csv(os.path.join(output_dir, 'dataframe.csv'), index=False)

    documents_v1 = df[columns_to_select].to_dict(orient='records')  
    # Convert dictionary to JSON object
    json_str = json.dumps(documents_v1)
    json_obj = json.loads(json_str)

    # Other way to upload docs, without batch (use when you have les than 900 docs, else check code below)
    def search_client_upload_docs(docs, index_name):
        search_client = SearchClient(service_endpoint, index_name, credential)
        logging.info(f"Uploading {len(docs)} documents to the index {index_name}")
        search_client.upload_documents(documents=docs)
        logging.info(f"Uploaded documents to the index {index_name}")
    
    search_client_upload_docs(json_obj, index_name)


def executeSearch(user_query):
    logging.info("Executing search...")
    index_name = os.environ["AZURE_SEARCH_INDEX"]
    service_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
    credential = AzureKeyCredential(os.environ["AZURE_SEARCH_ADMIN_KEY"]) if len(os.environ["AZURE_SEARCH_ADMIN_KEY"]) > 0 else DefaultAzureCredential()

    search_client = SearchClient(service_endpoint, index_name, credential)

    load_dotenv()

    def do_ai_search(user_query):
       
        embedded_query=generate_embeddings(user_query)

        vector = VectorizedQuery(
            vector=embedded_query,
            k_nearest_neighbors=3,
            fields="vector"
        ) 
        
        results = search_client.search(  
            search_text=user_query,  
            vector_queries=[vector], 
            select=[            
                'doc_name',            
                'h1',
                'h2',
                'h3',
                'text_content'
            ],
            search_fields=['doc_name','h1','h2','h3','text_content'],
            top=3
        )
        
        return results 

    ai_search_results = do_ai_search(user_query)    
    found_docs = get_string_results(ai_search_results)

    return found_docs

def analyze_file(document_intelligence_client, file_path):
    """Analyze the content of a single file using Azure Document Intelligence Client
    Args:
        document_intelligence_client (DocumentIntelligenceClient): The client to access the Azure Document Intelligence service.
        file_path (str): The path to the file to be analyzed
    """
    logging.info(f"Starting analysis of the file: {file_path}")
    with open(file_path, "rb") as f:
        file_bytes = f.read()
      
    logging.info("Sent files to Azure Document Intelligence service for processing...")
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout",
        body=file_bytes, 
        content_type="application/octet-stream",
        output_content_format="markdown",
    )
    logging.info("Waiting for results")
    result = poller.result()
    logging.info("Analysis complete.")
    return result.content

def process_file(file_path: str, document_intelligence_client, output_path: str, sleep_time: float = 1):
    """Process a single file using the Azure Document Intelligence Client.
    Args:
        file_path (str): The path to the file to be analyzed.
        document_intelligence_client (DocumentIntelligenceClient): The client to access the Azure Document Intelligence service.
        sleep_time (int): The number of seconds to wait between processing files to avoid hitting the rate limit.
    Returns:
        output_file_path (str): The path to the output markdown file.
    """
    logging.info(f"Processing file: {file_path}")
    file_name = os.path.basename(file_path)
    output_file_path = os.path.join(output_path, os.path.splitext(file_name)[0] +"_extracted.md")
    try:
        content = analyze_file(document_intelligence_client, file_path)
        with open(output_file_path, "w", encoding="utf-8") as markdown_file:
            markdown_file.write(content)
        logging.info(f"Analysis of {file_name} complete. Output saved to {output_file_path}")
    except Exception as e:
        logging.info(f"An error occurred while processing {file_name}: {e}")
    logging.info(f"Sleeping for {sleep_time} second(s) to avoid hitting the rate limit.")
    time.sleep(sleep_time)

    return output_file_path

def parse_markdown(md_text):
    html = markdown.markdown(md_text)
    soup = BeautifulSoup(html, features="html.parser")
    sections = []
    section = {"h1": "", "h2": "", "h3": "", "text_content": ""}
    for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'table']):
        if tag.name == 'h1':
            if section["text_content"]:
                sections.append(section)
                section = {"h1": "", "h2": "", "h3": "", "text_content": ""}
            section["h1"] = tag.text
        elif tag.name == 'h2':
            if section["text_content"]:
                sections.append(section)
                section = {"h1": section["h1"], "h2": "", "h3": "", "text_content": ""}
            section["h2"] = tag.text
        elif tag.name == 'h3':
            if section["text_content"]:
                sections.append(section)
                section = {"h1": section["h1"], "h2": section["h2"], "h3": "", "text_content": ""}
            section["h3"] = tag.text
        elif tag.name == 'p':
            section["text_content"] += tag.text + "\n"
        elif tag.name == 'table':
            section["text_content"] += str(tag) + "\n"
    if section["text_content"]:
        sections.append(section)
    return sections

def normalize_df(df):
    # Checking for null entries 
    null_count = df.isnull().sum()
    print(f"Found: {null_count} null values")
    
    # Filling null entries with "N/A" to avoid errors if data normalization is required 
    print("Filling null values with N/A")
    df.fillna("N/A", inplace=True)
    null_count = df.isnull().sum()
    print(f"Found: {null_count} null values")


def normalize_text(s, sep_token = " \n "):
    s = re.sub(r'\s+',  ' ', s).strip()
    s = re.sub(r". ,","",s)
    s = s.replace("..",".")
    s = s.replace(". .",".")
    s = s.replace("\n", "")
    s = s.strip()
    if not s:
        s = "N/A"    
    return s

def get_index(index_name,client):
    try:
        index = client.get_index(index_name)
        return index
    except ResourceNotFoundError as er:
        logging.info(er.message)
        return None

def delete_index(search_index_client,index_name):
    name = index_name
    search_index_client.delete_index(name)
    logging.info(f'{name} index correctly deleted')

def get_string_results(ai_search_results):
    vector_search_string_results=[]
    for result in ai_search_results:
        string_result=f"""         
        ###start_doc:
        Nombre documento: {result['doc_name']},
        Heading 1: {result['h1']},
        Heading 2: {result['h2']},
        Heading 3: {result['h3']},
        Contenido: {result['text_content']},
        ###end_doc
         """
        vector_search_string_results.append(string_result) 
    return "".join(vector_search_string_results)

async def section_builder(section_title, context_retrieval_service):
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(f'section: {str(section_title)}\n')
        context_documents = await context_retrieval_service.get_context(section_title)

        logging.info(f"Vector search finished for one query")
        f.write(f'context_documents for section: {str(section_title)}\n')
        f.write('---\n')

        result_openai = openai_search(context_documents, template_merged[section_title]["query"])
    
        logging.info(f"OpenAI answer for one query")

        result = result_openai.choices[0].message.content

    return result

def generate_embeddings(text):
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment="text-embedding-3-small",
        openai_api_version="2024-02-01",
    )
    return embeddings.embed_query(text)
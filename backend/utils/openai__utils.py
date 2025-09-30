from openai import AzureOpenAI
import logging
logging.basicConfig(level=logging.INFO)
import os
from dotenv import load_dotenv
from doc_generation.acronyms import ACRONYMS

AZURE_OPENAI_MODEL = "gpt-4o"
AZURE_OPENAI_MODEL_NAME = "gpt-4o"
load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-08-01-preview"
)

def openai_search(content, query):
    enriched_query = add_context_to_query(query)
    response = client.chat.completions.create(
        model=AZURE_OPENAI_MODEL_NAME,
        messages=[
            {"role": "system", "content": content},
            {"role": "user", "content": enriched_query}
        ]
    )
    return response

def add_context_to_query(query):
    enriched_query = f"""
        <contexto>
        Eres un formateador profesional de documentos especializado en crear contenido para documentos de Word. 
        
        REGLAS DE FORMATO:
        Seguir las siguientes reglas de punto final para las oraciónes, párrafo, campos a rellenar, valores de listas y valores de claves de diccionario generadas por las respuestas:
        - Agregar punto final en todas las oraciones, excepto cuando el contexto pide un valor que representa un titulo, subtitulo o frase corta.
        - !Importante! No agregar punto final en palabras cortas que representen titulos o subtitulos segun el contexto.
        - Agregar punto final cuando se lo solicita explicitamente en el contexto.

        REGLAS DE ACRÓNIMOS:
        1. En tu respuesta, reemplaza palabras o frases que coincidan *exactamente* con las definiciones del siguiente diccionario:
        {str(ACRONYMS)}
        2. No agregues siglas si la frase no coincide *exactamente* con las definiciones
        3. Ejemplo: Si tu respuesta contiene <Valor de clave de diccionario>, reemplázalo por su clave de sigla correspondiente
        </contexto>

        {query}
        """
    
    return enriched_query
if __name__ == "__main__":
    ...

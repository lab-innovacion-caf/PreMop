import os
import sys
import json
from docxtpl import DocxTemplate
import logging
def load_json_from_context(value):
    try:
        return json.loads(value)
    except:
        return []

def doc_s2_build(sections_dic):
    objetivo_general = load_json_from_context(sections_dic['S2_OBJETIVOS_GENERALES'])
    objetivo_general_desc = objetivo_general['objetivo_principal'] if 'objetivo_principal' in objetivo_general else ""
    objetivo_general_title = objetivo_general['titulo_objetivo'] if 'titulo_objetivo' in objetivo_general else ""

    dict_obj_especificos = load_json_from_context(sections_dic['S2_OBJETIVOS_ESPECIFICOS'])
    objetivos_especificos_lista = [
        {
            "titulo_objetivo_especifico": dict_obj_especificos[obj]["titulo_objetivo_especifico"],
            "objetivo_especifico":dict_obj_especificos[obj]["objetivo_especifico"]
        }   
        for obj in dict_obj_especificos
    ]

    componentes_data = load_json_from_context(sections_dic["S3_COMPONENTES_SUBCOMPONENTES"])
 
    indicadores_resultados = load_json_from_context(sections_dic["S4_INDICADORES_RESULTADOS"])
    indicadores_resultados_generales = indicadores_resultados.get("Objetivo General", [])
    indicadores_resultados_especificos = indicadores_resultados.get("Objetivo Específico", [])
    
    indicadores_productos = load_json_from_context(sections_dic["S4_INDICADORES_PRODUCTOS"])

    
    evolucion_indicadores_resultados = load_json_from_context(sections_dic["EVOLUCION_INDICADORES_RESULTADOS"])
    evolucion_indicadores_productos = load_json_from_context(sections_dic["EVOLUCION_INDICADORES_PRODUCTOS"])
    
    periodo_desembolso = evolucion_indicadores_resultados[0].get("periodo_desembolso")
    columnas_periodo_desembolso = [f"Año {i}" for i in range(1, len(periodo_desembolso))]
    columnas_periodo_desembolso.append("Año fin")

    financiamiento_componentes = load_json_from_context(sections_dic["S5_MATRIZ_FINANCIAMIENTO"])

    desembolsos_data = load_json_from_context(sections_dic["S3_CRONOGRAMA_DESEMBOLSOS"])
    
    anexo_tipo_proyecto = sections_dic["TIPO_PROYECTO"]
   
    costo_financiamiento = load_json_from_context(sections_dic["S13_COSTO_FINANCIAMIENTO"])
    
    context_merge = {
        "S2_OBJETIVOS_GENERALES_OBJETIVO_PRINCIPAL": objetivo_general_desc,
        "S2_OBJETIVOS_GENERALES_TITULO": objetivo_general_title,
        "S2_OBJETIVOS_ESPECIFICOS_LISTA": objetivos_especificos_lista,
        "S2_COMPONENTES_SUBCOMPONENTES": sections_dic["S2_COMPONENTES_SUBCOMPONENTES"],
        "S3_COMPONENTES": componentes_data,
        "S4_INDICADORES_RESULTADOS_GENERALES":indicadores_resultados_generales,
        "S4_INDICADORES_RESULTADOS_ESPECIFICOS":indicadores_resultados_especificos,
        "S4_INDICADORES_PRODUCTOS":indicadores_productos,
        "EVOLUCION_INDICADORES_RESULTADOS":evolucion_indicadores_resultados,
        "EVOLUCION_INDICADORES_PRODUCTOS":evolucion_indicadores_productos,
        "COLUMNAS_PERIODO_DESEMBOLSO":columnas_periodo_desembolso,
        "S5_COMPONENTES_FINANCIAMIENTO":financiamiento_componentes,
        "S3_CRONOGRAMA_DESEMBOLSOS":desembolsos_data,
        "ANEXO_TIPO_PROYECTO": anexo_tipo_proyecto,
        "S13_COSTO_FINANCIAMIENTO": costo_financiamiento
    }
    merge_context = {**sections_dic, **context_merge}
    template_file = "PREMOPTEMPLATE.docx"
    file_name = "generated_premop.docx"
    
    
    try:
        template_path = os.path.join(sys.path[0], "doc_generation", template_file)
        generated_doc_path = os.path.join(sys.path[0], "generated_files", file_name)
        doc = DocxTemplate(template_path)
        doc.render(merge_context)
        doc.save(generated_doc_path)

        return generated_doc_path 
    
    except Exception as e:
        logging.error(f"Error en doc_s2_build: {str(e)}")
        raise

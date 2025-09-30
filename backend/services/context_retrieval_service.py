from typing import Dict
import logging
from utils.openai__utils import openai_search
from doc_generation.template_dic import template_merged
from doc_generation.search_dic import search_queries


class ContextRetrievalService:
    def __init__(self):
        self._cache: Dict[str, str] = {}
    
    async def get_context(self, section_title):
        """
        Retrieves the context for the section title
        """
        from services.document_service import executeSearch
        context_key = template_merged[section_title]["context_key"]
        if context_key in self._cache:
            logging.info(f"Cache hit for section: {section_title}")
            return self._cache[context_key]

        if section_title == 'S4_INDICADORES_RESULTADOS':
            context_documents = await self.get_s4_indicadores_resultados_context()
        else:
            context_documents = executeSearch(search_queries[context_key])

        self._cache[context_key] = context_documents
        return context_documents
    
    async def get_s4_indicadores_resultados_context(self):
        from services.document_service import executeSearch
        context_documents1 = executeSearch(search_queries['OBJETIVOS'])

        context_search_query1 = '''
            Solicito una respuesta para el siguiente requerimiento pero no me des una mensaje previo a responderme.
            En base a la información obtenida, dame la descripción completa de "Objetivo General" y de "Objetivos específicos" en el siguiente formato:
                Objetivo General: <Descripción completa del objetivo general>
                Objetivos Específicos: <Descripción completa de los objetivos específicos>
        '''
        result_openai1 = openai_search(context_documents1, context_search_query1)

        context_documents2 = executeSearch(search_queries['MATRIZ_INDICADORES'])
        context_search_query2 = '''
            En base a la informacion obtenida, por cada fila de la tabla de la seccion "indicadores de resultados", genera una lista de indicadores de productos con el siguiente formato 
            {
                "componente":"<Columna 'Componentes'>",
                "unidad":"<Valor exacto de la columna 'Año 4 Metas' o 'Metas'>
                "medio_verificacion":"<Columna 'Método de cálculo' o 'Medio de verificación'>"
            }
            Importante: Solamente extraer los indicadores de resultados, no incluir los indicadores de productos.
        '''
        result_openai2 = openai_search(context_documents2, context_search_query2)

        return result_openai1.choices[0].message.content + "\n" + result_openai2.choices[0].message.content
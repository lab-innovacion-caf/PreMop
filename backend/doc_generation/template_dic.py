from doc_generation.queries_dic import user_queries

template_merged = {
    'S1_PROYECTO_PROGRAMA': {
        "context_key": 'RESUMEN_EJECUTIVO',
        "query": user_queries['S1_PROYECTO_PROGRAMA']
    },
    'S1_NOMBRE_DEL_ORGANISMO_EJECUTOR': {
        "context_key": 'RESUMEN_EJECUTIVO',
        "query": user_queries['S1_NOMBRE_DEL_ORGANISMO_EJECUTOR']
    },
    'S1_NOMBRE_CON_ARTICULO_ORGANISMO_EJECUTOR': {
        "context_key": 'RESUMEN_EJECUTIVO',
        "query": user_queries['S1_NOMBRE_CON_ARTICULO_ORGANISMO_EJECUTOR']
    },
    'S2_OBJETIVOS_GENERALES': {
        "context_key": 'OBJETIVOS',
        "query": user_queries['S2_OBJETIVOS_GENERALES']
    },
    'S2_OBJETIVOS_ESPECIFICOS': {
        "context_key": 'OBJETIVOS',
        "query": user_queries['S2_OBJETIVOS_ESPECIFICOS']
    },
    'S2_COMPONENTES_SUBCOMPONENTES': {
        "context_key": 'COMPONENTES_SUBCOMPONENTES',
        "query": user_queries['S2_COMPONENTES_SUBCOMPONENTES']
    },
    'S3_COMPONENTES_SUBCOMPONENTES': {
        "context_key": 'COMPONENTES_SUBCOMPONENTES',
        "query": user_queries['S3_COMPONENTES_SUBCOMPONENTES']
    },
    'S4_INDICADORES_RESULTADOS': {
        "context_key": '',
        "query": user_queries['S4_INDICADORES_RESULTADOS']
    },
    'S4_INDICADORES_PRODUCTOS': {
        "context_key": 'MATRIZ_INDICADORES',
        "query": user_queries['S4_INDICADORES_PRODUCTOS']   
    }
    ,
    'EVOLUCION_INDICADORES_RESULTADOS': {
        "context_key": 'MATRIZ_INDICADORES',
        "query": user_queries['EVOLUCION_INDICADORES_RESULTADOS']
    },
    'EVOLUCION_INDICADORES_PRODUCTOS': {
        "context_key": 'MATRIZ_INDICADORES',
        "query": user_queries['EVOLUCION_INDICADORES_PRODUCTOS']
    },
    'S5_MATRIZ_FINANCIAMIENTO': {
        "context_key": 'COSTO_FINANCIAMIENTO',
        "query": user_queries['S5_MATRIZ_FINANCIAMIENTO']
    },
    'S3_CRONOGRAMA_DESEMBOLSOS': {
        "context_key": 'CRONOGRAMA_DESEMBOLSOS',
        "query": user_queries['S3_CRONOGRAMA_DESEMBOLSOS']
    },
    'TIPO_PROYECTO': {
        "context_key": 'DESCRIPCION_ALCANCE_PROYECTO',
        "query": user_queries['TIPO_PROYECTO']
    },
    'S13_COSTO_FINANCIAMIENTO': {
        "context_key": 'COSTO_FINANCIAMIENTO',
        "query": user_queries['S13_COSTO_FINANCIAMIENTO']
    }
}

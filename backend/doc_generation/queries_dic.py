user_queries = {
    
    "S1_PROYECTO_PROGRAMA": "Responde únicamente con el Nombre de la operación mencionado en el texto, sin ninguna introducción o frase adicional",
    
    "S1_NOMBRE_DEL_ORGANISMO_EJECUTOR": '''
        Responde únicamente con el valor del campo "Organismo Ejecutor" (o el valor del campo "Coordinador Tecnico" en caso de que no lo haya) mencionado en el texto, sin ninguna introducción o frase adicional
        En caso de no estar definido, responde con un string vacío.
    ''',
    
    "S1_NOMBRE_CON_ARTICULO_ORGANISMO_EJECUTOR": '''
        Extrae el organismo ejecutor o coordinador técnico del texto siguiente, aplicando estas reglas en orden:

        1. Busca el valor asociado al campo "Organismo Ejecutor"
        2. Si no existe, busca el valor asociado al campo "Coordinador Tecnico"
        3. Si se encuentra un valor, agrégale el artículo correspondiente en minúscula:
        4. Si no se encuentra ningún valor, devuelve un string vacío ""

        Formato de la respuesta:
        - Solo el texto encontrado con su artículo
        - Sin puntuación final
        - Sin frases adicionales ni explicaciones

        Ejemplos:

        Entrada 1:
        "Organismo Ejecutor: Banco Mundial"
        Salida 1: "el Banco Mundial"

        Entrada 2:
        "Coordinador Tecnico: Universidad Nacional"
        Salida 2: "la Universidad Nacional"
    ''',

    "S2_OBJETIVOS_GENERALES": '''
        Solicito una respuesta para el siguiente requerimiento pero no me des una mensaje previo a responderme.
        En base a esta informacion obtenida extrae genera un diccionario con el siguiente formato:
        {	
            "titulo_objetivo": "<Necesito crear un título para el objetivo general, El título debe ser breve y reflejar el enfoque del proyecto.>",
            "objetivo_principal": "<deben ser completados con la descripción completa del objetivo general.>"
        }
        Devuelve únicamente el objeto JSON. No incluyas comentarios, explicaciones, etiquetas Markdown (como ```json), ni texto adicional fuera del JSON. 
    ''',
    
    "S2_OBJETIVOS_ESPECIFICOS": '''
        En base a esta información proporcionada, genera un diccionario de los objetivos específicos en formato JSON válido. Sigue estas instrucciones:
        1. Numera cada elemento del diccionario como una clave de tipo string (e.g., "1", "2", "3").
        2. Para cada clave, incluye dos campos:
            - "titulo_objetivo_especifico": "<Crea un título para el objetivo especifico. El título debe ser breve y reflejar el enfoque del proyecto>",
            - "objetivo_especifico": "<Descripción completa del objetivo específico>"
        3. Devuelve únicamente el objeto JSON. No incluyas comentarios, explicaciones, etiquetas Markdown (como ```json), ni texto adicional fuera del JSON. 
    ''',
    
    "S2_COMPONENTES_SUBCOMPONENTES": '''
        En base a la informacion proporcionada, extraer y listar Componentes y Subcomponentes. Responde unicamente con la informacion obtenida, evita agregar una introduccion o contexto.
        Existen 2 casos, por ejemplo:
        Caso 1: Nombre y numeracion:
            'Componente' <numero_componente>: <descripcion del componente>.
                'Subcomponente' <numero_componente>.<numero_subcomponente> : <descripcion del subcomponente>
        Caso 2: solamente numeracion:
            <numero_componente> : <descripcion del componente>
                <numero_componente>.<numero_subcomponente>  : <descripcion del subcomponente>
        Una vez identificados los Componentes y sus correspondientes Subcomponentes, genera una lista con el siguiente formato, evita agregar una introduccion o un contexto:
        Componente 1. <descripcion del Componente>
            Subcomponente 1.1. <descripcion del Subcomponente>,   

        Piensa paso a paso y no crees subcomponentes que no existan en el texto proporcionado, guiarse por si no tienen una numeracion explicita
    ''',

    "S3_COMPONENTES_SUBCOMPONENTES": '''
            En base a este resultado, responde únicamente con una lista de diccionarios en el siguiente formato. Evita agregar cualquier contexto o explicación adicional, responde estrictamente con la información requerida:
            
            {
                "indice": "<Numero de componente/subcomponente> Se refiere al indice (Ejemplo: 1, 1.1, 1.2, 2, 2.1, 2.2)",
                "titulo": "<Crear un titulo para el componente/subcomponente especifico. El Título debe ser breve y reflejar el enfoque de la descripcion>",
                "descripcion": "<Crear un breve resumen sobre la descripción completa del componte/subcomponente> Si es un componente con subcomponentes, el campo "descripcion" para ese componente debe ser un string vacío."
            },
            
            Aclaraciones:
            - No crear subcomponentes que no existan en el texto proporcionado, guiarse por si no tienen una numeracion explicita

            Ejemplo de texto de componentes/subcomponententes de entrada:
                Componente 1: Infraestructura educativa. Incluye la construcción de nuevos edificios y refacción de infraestructura existente. Este componente financiará los siguientes subcomponentes, a saber: 
                    1.1. Ampliación y mejoramiento de la cobertura. Obras nuevas y refacciones, equipamiento 
                    nuevo y sustitución de equipamiento por obsolescencia, así como construcción y 
                    equipamiento de comedores escolares, a fin de ampliar la cobertura y calidad edilicia. 
                    1.2. Preinversión y supervisión. Preinversión y supervisión técnica y ambiental de obras, 
                    para el desarrollo de proyectos ejecutivos, desarrollo de un sistema de gestión de 
                    infraestructura  y reforzar la capacidad institucional de la Provincia. 
                Componente 2: vinculación con el Contexto Productivo. Incluye la adquisición de equipamiento 
                    para aulas taller fijas y móviles para dictado de capacitaciones en escuelas secundarias orientadas, 
                    la adquisición de equipos para un centro de simulación y recursos para el fortalecimiento del área 
                    sustantiva y asistencia técnica requerida para el desarrollo del componente. 
                Componente 3: Administración del Programa. Prevé recursos para brindar apoyo a la gestión 
                    del Programa para actividades de administración, monitoreo, supervisión y evaluación, la ejecución 
                    de la auditoria externa de la operación, y los gastos de evaluación y la comisión de financiamiento 
                    del préstamo CAF

            Salida deseada:
            [
                {
                    "indice": "1",
                    "titulo": "Infraestructura educativa",
                    "descripcion": ""
                },
                {
                    "indice": "1.1",
                    "titulo": "Ampliación y mejoramiento de la cobertura",
                    "descripcion": <Breve resumen de la descripción>
                },
                {
                    "indice": "1.2",
                    "titulo": "Preinversión y supervisión",
                    "descripcion": <Breve resumen de la descripción>
                },
                {
                    "indice": "2",
                    "titulo": "Vinculación con el Contexto Productivo",
                    "descripcion": <Breve resumen de la descripción>
                },
                {
                    "indice": "3",
                    "titulo": "Administración del Programa",
                    "descripcion": <Breve resumen de la descripción>
                }
            ]
            Importante, tener en cuenta que los titulos de los componentes/subcomponentes nunca pueden ser "Componente 1", "Componente 2", etc. Siempre deben ser los titulos mencionados en la tabla del contexto
            Responde estrictamente en formato json, sin markdown y con los datos correspondientes
            ''',
    "S4_INDICADORES_PRODUCTOS": '''
        En base a la informacion obtenida, por cada fila de la tabla de indicadores con columnas Componente, valor de los indicadores y Medio de verificacion, obtener la seccion "indicadores de productos", luego por cada fila de esta seccion genera una lista de indicadores de productos con el siguiente formato, teniendo en cuenta que los indicadores de productos viene segregados por componentes 
        {
            "nro_componente":"<Numero de componente al cual pertenecen los indicadores>",
            "indicadores":[
                {
                    "componente":"<Columna 'Componentes' de la matriz/tabla de indicadores>",
                    "unidad":"<Valor exacto de la columna 'Año 4 Metas' o 'Metas'>
                    "medio_verificacion":"<Columna 'Método de cálculo' o 'Medio de verificación'>"
                },
            ]
        }            
        Devolver la lista de indicadores de productos sin agregar contexto adicional ni formato markdown
    ''',

    "S4_INDICADORES_RESULTADOS": '''
        En base a la definicion de los objetivos y la lista de indicadores, agrupa los indicadores de la lista conforme a las siguientes claves:
        1. Objetivo General
        2. Objetivo Específico
        Instrucciones para agrupar los indicadores:
        - Analiza cada indicador paso a paso, y, en funcion de su componente y unidad, determina si está alineado con el **Objetivo General** o con alguno de los **Objetivos Específicos**.
        - Utiliza las siguientes pautas para la agrupación:
            - Si el indicador refleja **el impacto global** o resultados amplios que abarcan todo el programa, agrúpalo bajo el **Objetivo General**.
            - Si el indicador está directamente relacionado con una acción puntual, específica o detallada mencionada en los **Objetivos Específicos**, agrúpalo en el objetivo correspondiente.
            - Tener en cuenta que un indicador general puede estar dado por la sumatoria de varios indicadores específicos.
        Instrucciones de formato de salida:
            - Presenta los resultados agrupados bajo un diccionario con las claves "Objetivo General" y "Objetivo Específico"
            - Devolver en formato json, sin utilizar formato mardown y sin agregar texto adicional. Importante, no agregar formato markdown.
    
        Ejemplo de pensamiento:
        Tengo la siguiente lista de indicadores:
        [
            {
                "componente": "Número de estudiantes beneficiados por proyectos de educación (#)",
                "unidad": "29.900",
                "medio_verificacion": "Informe del MED"
            },
            {
                "componente": "Número de estudiantes matriculados en unidades educativas de edificios nuevos, desagregado por género y nivel educativo",
                "unidad": "13.400",
                "medio_verificacion": "Informe del MED de oferta educativa por modalidad, nivel educativo por localidad"
            },
            {
                "componente": "Número de estudiantes de escuelas secundarias técnicas cursando los nuevos diseños curriculares",
                "unidad": "9.000",
                "medio_verificacion": "Informes anuales de Dirección de Monitoreo y Evaluación Educativa"
            },
            {
                "componente": "Número de estudiantes de secundaria que recibieron capacitación laboral por proyecto bittitulación",
                "unidad": "7.500",
                "medio_verificacion": "Informes de Dirección de Monitoreo y Evaluación Educativa"
            },
            {
                "componente": "Tasa de egreso del nivel secundario en escuelas intervenidas por proyecto de bittitulación",
                "unidad": "65%",
                "medio_verificacion": "Informes de Dirección de Monitoreo y Evaluación Educativa"
            }
        ]
        En este caso, agruparía los indicadores de la siguiente manera:
            {
                "Objetivo General": [
                    {
                        "componente": "Número de estudiantes beneficiados por proyectos de educación (#)",
                        "unidad": "29.900",
                        "medio_verificacion": "Informe del MED"
                    }
                ],
                "Objetivo Específico": [
                    {
                        "componente": "Número de estudiantes matriculados en unidades educativas de edificios nuevos, desagregado por género y nivel educativo",
                        "unidad": "13.400",
                        "medio_verificacion": "Informe del MED de oferta educativa por modalidad, nivel educativo por localidad"
                    },
                    {
                        "componente": "Número de estudiantes de escuelas secundarias técnicas cursando los nuevos diseños curriculares",
                        "unidad": "9.000",
                        "medio_verificacion": "Informes anuales de Dirección de Monitoreo y Evaluación Educativa"
                    },
                    {
                        "componente": "Número de estudiantes de secundaria que recibieron capacitación laboral por proyecto bittitulación",
                        "unidad": "7.500",
                        "medio_verificacion": "Informes de Dirección de Monitoreo y Evaluación Educativa"
                    },
                    {
                        "componente": "Tasa de egreso del nivel secundario en escuelas intervenidas por proyecto de bittitulación",
                        "unidad": "65%",
                        "medio_verificacion": "Informes de Dirección de Monitoreo y Evaluación Educativa"
                    }
                ]
            }
            Ya que la sumatoria de las unidades de los indicadores específicos (13400 + 9000 + 7500) es igual a 29900.
        
        Devolver el resultado en formato json, sin utilizar formato mardown y sin agregar texto adicional. Importante, no agregar formato markdown.
        ''', 

    "EVOLUCION_INDICADORES_RESULTADOS": '''
        Analiza la tabla de indicadores y devuelve un arreglo de diccionarios que contenga SOLO los indicadores de resultados. Para cada indicador, genera un diccionario con el siguiente formato dinámico:
        {
            "componente": [Valor exacto de la columna Componentes],
            "base": [valor exacto de la columna Linea Base],
            "periodo_desembolso": [Una lista de valores donde se genera dinámicamente los valores de las columnas "ano_N" bajo la columna "Periodo de desembolsos"],
            "meta": [valor exacto de la última columna antes de "Medio de Verificación", representa la meta y puede variar entre Meta o Año n Meta]
        }
        Consideraciones importantes:
        - Extraer ÚNICAMENTE los indicadores bajo el encabezado "Indicadores de resultados"
        - Detectar automáticamente todas las columnas de años presentes en "Periodo de desembolsos"
        - Generar los valores "ano_1", "ano_2", "ano_3", etc. según el número de columnas de años encontradas
        - La clave "meta" debe tomar el valor exacto de la columna (sea "Metas año N" o similar)
        - Incluir todos los campos aunque el valor sea 0 o vacio
        - Devolver la lista sin agregar contexto adicional ni formato markdown

        Ejemplo de estructura para validación:
        Si hay 3 años: {..., periodo_desembolso: ["valor año 1", "valor año 2", "valor año 3"] "meta": M}
        Si hay 4 años: {..., periodo_desembolso: ["valor año 1", "valor año 2", "valor año 3", "valor año 4"] "meta": M}
    ''',

    "EVOLUCION_INDICADORES_PRODUCTOS": '''
        FUNCIÓN: Extracción y Estructuración de Indicadores de Producto

        ENTRADA:
        - Tabla con indicadores de desempeño que incluye sección "Indicadores de producto"

        SALIDA:
        Lista de diccionarios con la siguiente estructura por cada indicador de producto:
        {
            "componente": str,  # Título textual del componente (ej: "Desarrollo de infraestructura")
            "base": str | float,  # Valor de Línea Base
            "periodo_desembolso": list[str | float],  # Valores anuales del período de desembolso
            "meta": str | float  # Valor final de meta
        }

        REGLAS DE PROCESAMIENTO:

        1. ALCANCE
        - Procesar EXCLUSIVAMENTE indicadores bajo la sección "Indicadores de producto"
        - Ignorar cualquier otro tipo de indicador (resultado, impacto, etc.)
       
        2. ESTRUCTURA DE DATOS
        - componente: 
            * Extraer título descriptivo exacto
            * NO incluir numeración (ej: "Componente 1")
            * Preservar texto completo del componente
        - base:
            * Valor exacto de "Línea Base"
            * Mantener formato original (numérico/texto)
        - periodo_desembolso:
            * Detectar automáticamente número de años en sección "Periodo de desembolsos"
            * Crear lista con valor para cada año detectado
            * Preservar orden cronológico
        - meta:
            * Extraer último valor antes de "Medio de Verificación"
            * Adaptar a variaciones en nombre (Meta, Año n Meta, etc.)
            * Copiar el valor exacto de la columna "Meta" o "Año n Meta"

        3. MANEJO DE DATOS
        - Preservar valores nulos como "" o 0 según formato original
        - No omitir campos aunque estén vacíos
        - Mantener tipos de datos originales (texto/número)
        - Todas las filas deben tener la misma cantidad de columnas

        4. FORMATO DE RESPUESTA
        - Retornar lista de diccionarios sin formato adicional
        - No incluir markdown ni texto explicativo
        - No agregar metadatos o contexto

        EJEMPLOS DE VALIDACIÓN:

        Para 3 años:
        [{
            "componente": "Título real del componente",
            "base": "Valor base",
            "periodo_desembolso": ["2024", "2025", "2026"],
            "meta": "Valor meta"
        }]

        Para 4 años:
        [{
            "componente": "Título real del componente",
            "base": "Valor base",
            "periodo_desembolso": ["2024", "2025", "2026", "2027"],
            "meta": "Valor meta"
        }]
    ''',

    "S5_MATRIZ_FINANCIAMIENTO": '''
        En base al contexto proporcionado, genera una lista donde sus elementos vienen dados por las fila de la tabla COSTO POR COMPONENTE Y FUENTES DE FINANCIAMIENTO, recorre fila por fila y genera un diccionario con el siguiente formato: 
            {
                "es_componente": "<True si es un componente, False si es un subcomponente>" (Viene dado por la numeracion, por ejemplo 1.1 es un subcomponente, 1 es componente)
                "componente": "<Valor exacto de la columna Componente>",
                "caf": "<Valor exacto de la columna CAF>",
                "local": "<Valor exacto de la columna Aporte Local>",
                "total": "<Valor exacto de la columna Total>",
                "porcentaje": "<Valor exacto de la columna Porcentaje (%)>"
            }
        Responder únicamente con la información solicitada, sin agregar ningún tipo de contexto adicional ni formato markdown
    ''',

    "S3_CRONOGRAMA_DESEMBOLSOS": '''
    En base al contexto proporcionado, genera una lista donde sus elementos vienen dados por las fila de la tabla CRONOGRAMA TENTATIVO DE DESEMBOLSO, recorre fila por fila y genera un diccionario con el siguiente formato: 
    {
        "fuente": "<Valor exacto de la columna Fuente, en si no se encuentra esa columna, es el valor de la primer columna>",
        "ano1": "<Valor exacto de la columna Año 1>",
        "ano2": "<Valor exacto de la columna Año 2>",
        "ano3": "<Valor exacto de la columna Año 3>",
        "ano4": "<Valor exacto de la columna Año 4>",
        "total": "<Valor exacto de la columna Total>"
    }
    Consideraciones a tener en cuenta:
    - Utiliza el valor "Préstamo CAF" en caso que el valor de la columna fuente sea uno de los siguientes:
        - "Monto".
        - "En USD MM"
        Responder únicamente con la información solicitada, sin agregar ningún tipo de contexto adicional ni formato markdown
    ''',

    "TIPO_PROYECTO": '''
       En base al contexto, inferir el tipo de proyecto al que se esta haciendo referencia.
        Las dos opciones posibles de proyecto son: EDUCACIÓN y SALUD
        Responder únicamente con las opciones proporcionadas, sin agregar ningún tipo de contexto adicional ni formato markdown
        En caso de que el tipo de proyecto no haga referencia a ninguna de las opciones, responder con un string vacío.
    ''',

    "S13_COSTO_FINANCIAMIENTO": '''
        Extrae la siguiente información financiera del texto proporcionado y devuélvela en formato JSON:
        1. Extrae el costo total del programa 
        2. Extrae la contribución de CAF junto con su porcentaje respecto al costo total (incluye el porcentaje entre paréntesis)
        3. Si se menciona aporte local, inclúyelo como un campo separado con su valor y porcentaje entre paréntesis
        La estructura JSON debe seguir este formato:
        {
            "costo_total": str: <número>,
            "aporte_caf": str: "<número> (<porcentaje>%)",
            "aporte_local": str: "<número> (<porcentaje>%)" // Si no se menciona aporte local, dejarlo como 0 (0%)
        }
        Ejemplo de Entrada:
        "El costo total del Programa es de USD 60 MM. De este monto, USD 60 MM corresponden al préstamo CAF (100,0%), y no se prevé aporte local."

        Salida Esperada:
        {
            "costo_total": "60.000.000",
            "aporte_caf": "60.000.000 (100%)",
            "aporte_local": "0 (0%)" 
        }

        Ejemplo de Entrada 2:
        "El costo total del Programa es de USD 100 MM. De este monto, USD 80 MM corresponden al préstamo CAF (80,0%), y USD 20 MM corresponden al aporte local."

        Salida Esperada 2:
        {
            "costo_total": "100.000.000",
            "aporte_caf": "80.000.000 (80%)",
            "aporte_local": "20.000.000 (20%)"
        }

        PENSAMIENTO PARA EXTRAER LOS MONTOS:
        - Identificar valores monetarios expresados en USD o MM
        - Convertir valores en MM a números completos (1 MM = 1.000.000)
        - Extraer solo valores numéricos sin símbolos de moneda
        - Incluir los puntos en los numeros, es decir por ejemplo1.000.000

        FORMATO DE RESPUESTA
        - Retornar solo el objeto JSON
        - No incluir texto adicional ni markdown
        - Incluir los puntos en los numeros 
    ''',
} 
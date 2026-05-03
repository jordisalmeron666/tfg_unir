# tfg_unir

## ¿Qué problema concreto resuelve el sistema?

Este sistema responde preguntas en lenguaje natural sobre manuales y reglamentos de wargames de miniaturas. Permite a los usuarios consultar dudas específicas sobre reglas, escenarios, campañas, facciones y equipamiento de varios juegos, obteniendo respuestas precisas y fundamentadas en los textos originales de los manuales indexados.

## ¿Qué necesita hacer el sistema y bajo qué restricciones?

- **Indexar**: El sistema debe procesar e indexar los documentos y manuales de diferentes wargames, organizando la información por secciones (reglas, escenarios, facciones, etc.).
- **Responder preguntas**: Debe recibir preguntas en lenguaje natural (por ejemplo, vía Telegram) y buscar la respuesta en los manuales indexados.
- **Restricciones**:
  - Solo puede responder usando la información realmente contenida en los manuales indexados.
  - Si no encuentra suficiente contexto, debe indicarlo claramente.
  - No debe inventar información ni interactuar como un chatbot tradicional.

## ¿Cómo está diseñado y construido?

- **Backend en Python**: Utiliza Python y varias librerías para el procesamiento de lenguaje natural y la gestión de bases de datos vectoriales.
- **Indexación**: Usa LlamaIndex y ChromaDB para crear índices vectoriales de los manuales.
- **Modelo LLM**: Se apoya en modelos de Azure OpenAI para interpretar preguntas y generar respuestas.
- **Interfaz Telegram**: El sistema se controla y consulta principalmente a través de un bot de Telegram.
- **Configuración modular**: Cada juego tiene su propia colección y secciones configuradas en el sistema.

## ¿Dónde está el código y cómo se organiza?

- El código fuente está en este repositorio de GitHub.
- Estructura principal:
  - main.py: Lógica del bot y punto de entrada.
  - llm_handler.py: Orquestación de preguntas y respuestas usando LLM y herramientas.
  - indexer.py: Indexación de documentos y manuales.
  - indexes.py: Configuración de los índices y secciones por juego.
  - config.py: Configuración general y de servicios externos.
  - files: Carpeta con los manuales y documentos de cada juego, organizados por subcarpetas.
  - doc: (Ver documentación técnica detallada aquí).

## ¿Qué funcionalidad se ha conseguido realmente?

- Indexación automática de manuales de varios wargames.
- Respuestas a preguntas en lenguaje natural sobre reglas, escenarios, campañas y facciones, citando siempre la fuente.
- Integración con Telegram para consulta directa.
- Restricción efectiva para no inventar respuestas fuera del contexto indexado.

# Asesor de Optimización de CV con IA

Este proyecto es una aplicación interactiva desarrollada con Streamlit que utiliza Modelos de Lenguaje Grandes (LLMs) y técnicas de Recuperación Aumentada por Generación (RAG) para ayudar a los usuarios a optimizar su Currículum Vitae (CV) basándose en una Descripción de Puesto de Trabajo (DPT) específica.

---

## Funcionalidades

* **Carga de CV:** Permite subir un CV en formato PDF.
* **Entrada de DPT:** El usuario puede pegar la descripción del puesto de trabajo deseado.
* **Análisis y Sugerencias:** La aplicación resume la DPT, extrae información relevante del CV y genera sugerencias de optimización para adaptar el CV al puesto.
* **Chat Interactivo:** Un asistente de IA con capacidad de chat para responder preguntas adicionales sobre las sugerencias o el proceso de optimización.

---

## Cómo Funciona

1.  El usuario sube su CV en formato PDF.
2.  La DPT es resumida usando un modelo de Cohere.
3.  El CV se procesa y se divide en fragmentos, los cuales se convierten en embeddings (representaciones numéricas).
4.  Estos embeddings se almacenan en una base de datos vectorial **FAISS**.
5.  Cuando el usuario solicita sugerencias, la aplicación utiliza el resumen de la DPT y el contexto relevante del CV (obtenido vía RAG desde FAISS) para generar una respuesta detallada con un LLM de Cohere.
6.  El historial de chat se mantiene para conversaciones contextuales.

---

## Despliegue

Esta aplicación está diseñada para ser desplegada en **Streamlit Cloud**.

### Requisitos

Asegúrate de tener un archivo `requirements.txt` en la raíz de tu repositorio con las siguientes dependencias:

streamlit  
langchain-core  
langchain-community[faiss]  
langchain-cohere  
PyMuPDF  
python-dotenv  
requests  
tenacity  
cohere  
protobuf==3.20.1  
numpy==1.26.4  
faiss-cpu  


### Configuración de Claves de API  

Para que la aplicación funcione, necesitas una **clave API de Cohere**. Es crucial que **no la incluyas directamente en tu código o repositorio**. Configúrala como un "Secret" en Streamlit Cloud bajo el nombre `COHERE_API_KEY`. Ten en cuenta que, aunque Cohere tenga un nivel de uso gratuito, el consumo de la API se contabilizará bajo tu cuenta.  

### Versión de Python  

Es vital seleccionar una versión de Python compatible en Streamlit Cloud. Se recomienda usar **Python 3.10** o **Python 3.11** para el despliegue de esta aplicación.  

---

## Uso Local (Desarrollo)  

Para ejecutar este proyecto en tu máquina:  

1.  Clona el repositorio: `git clone [URL_DE_TU_REPOSITORIO]`  
2.  Accede al directorio del proyecto: `cd [nombre_de_tu_carpeta_proyecto]`  
3.  Instala los requirements anteriores  
4.  Crea un archivo `.env` en la raíz del proyecto y añade tu clave API:  
    ```
    COHERE_API_KEY="tu_clave_api_de_cohere_aqui"  
    ```
5.  Ejecuta la aplicación: `streamlit run app_cv/app_cv.py`  

Aquí tienes el [enlace](https://boostyourcv.streamlit.app/) para ver la app en Streamlit Cloud

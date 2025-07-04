# 📄 Asesor Personal de CV con IA y RAG

---

Este proyecto es una **aplicación interactiva desarrollada con Streamlit** que explora la aplicación de **Modelos de Lenguaje Grandes (LLMs)** y técnicas de **Recuperación Aumentada por Generación (RAG)**. Su propósito es experimentar con la optimización de un Currículum Vitae (CV) en base a una Descripción de Puesto de Trabajo (DPT) específica.

---

## Funcionalidades

* **Carga de CV:** Permite cargar un CV en formato PDF.
* **Entrada de DPT:** Facilita la introducción de una descripción de puesto de trabajo.
* **Análisis y Sugerencias:** La aplicación procesa la DPT y el CV para generar sugerencias que adapten el CV al contexto del puesto.
* **Chat Interactivo:** Incluye un asistente de IA conversacional para interactuar con las sugerencias generadas.

---

## Cómo Funciona

1.  El usuario sube su CV en formato PDF.
2.  La DPT se resume utilizando un modelo de Cohere.
3.  El CV se procesa y fragmenta, generando embeddings (representaciones numéricas).
4.  Estos embeddings se indexan en una base de datos vectorial **FAISS**.
5.  Para generar sugerencias, la aplicación utiliza el resumen de la DPT y recupera contexto relevante del CV (vía RAG desde FAISS), procesándolo con un LLM de Cohere.
6.  Se mantiene un historial para el chat, permitiendo conversaciones contextuales.

---


## Uso Local (Desarrollo)

Para ejecutar este proyecto en tu máquina:

1.  Clona el repositorio: `git clone [URL_DE_TU_REPOSITORIO]`
2.  Accede al directorio del proyecto: `cd [nombre_de_tu_carpeta_proyecto]`
3.  Instala las dependencias listadas en los requisitos.
4.  Crea un archivo `.env` en la raíz del proyecto y añade tu clave API:
    ```
    COHERE_API_KEY="tu_clave_api_de_cohere_aqui"
    ```
5.  Ejecuta la aplicación: `streamlit run app_cv/app_cv.py`

Puedes ver la aplicación desplegada en Streamlit Cloud [aquí](https://boostyourcv.streamlit.app/).
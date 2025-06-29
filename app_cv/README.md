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
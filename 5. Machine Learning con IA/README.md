# 📸 AI Health Predictor: Predicción de Riesgo Cardiovascular con Visión por Computadora y LLMs

---

Les presento este emocionante proyecto donde fusionamos el poder de la Inteligencia Artificial para abordar un problema de salud crítico: la predicción del riesgo cardiovascular. En este repositorio, verán cómo la combinación de modelos de lenguaje grandes (LLMs) y el aprendizaje automático tradicional puede crear una herramienta innovadora y perspicaz.

## 🌟 La Visión del Proyecto

Como entusiasta de la ciencia de datos y la IA, siempre busco formas de aplicar estas tecnologías para resolver problemas del mundo real. Este proyecto es un claro ejemplo de cómo la IA puede ir más allá de las aplicaciones convencionales para ofrecer soluciones tangibles en áreas como la salud.  

Imagina un futuro donde una simple imagen pueda ofrecer una primera aproximación a nuestro bienestar. Este proyecto busca ser un paso en esa dirección, mostrando el potencial de la IA para democratizar el acceso a insights de salud preliminares y fomentar la conciencia.

## ✨ ¿Cómo Funciona?

Este sistema es una orquesta de tecnologías trabajando en armonía:

1.  **Captura de Imagen:** Le proporcionamos una fotografía de una persona a nuestro script de Python.
2.  **Visión por Computadora (a través de LLM):** La imagen se envía a un **Modelo de Lenguaje Grande (LLM)** avanzado (en este caso, Gemini 2.5 Flash), que no solo procesa texto, ¡sino también imágenes! Este LLM actúa como nuestro "ojo" inteligente, analizando la foto para extraer características físicas clave:
    * **Índice de Masa Corporal (IMC):** Estimado en formato `float`.
    * **Edad:** Un valor `int` aproximado.
    * **Sexo:** `0` para hombre, `1` para mujer.
    * **Ojeras:** `0` si no se aprecian, `1` si sí.
    * **Tabaquismo:** `0` si hay indicios, `1` si no los hay.
3.  **Justificación Inteligente:** Lo más fascinante es que el LLM no solo devuelve los valores, ¡sino que también proporciona una **justificación detallada y coherente** de por qué ha asignado cada uno de esos parámetros! Esto añade una capa crucial de interpretabilidad a nuestro sistema.
4.  **Predicción de Machine Learning:** Los valores numéricos obtenidos del LLM (`[IMC, Edad, Sexo, Ojeras, Tabaquismo]`) se alimentan a un modelo de Machine Learning (`best_model.pkl`) previamente entrenado. Este modelo se encarga de calcular el **riesgo cardiovascular** de la persona, clasificándolo en:
    * **Bajo**
    * **Medio**
    * **Alto**
5.  **Resultado Final:** El script final combina la predicción del riesgo cardiovascular con la justificación del LLM, proporcionando un resultado completo y fácil de entender.

## 🛠️ Tecnologías Utilizadas

* **Python:** El lenguaje de programación principal.
* **Google Gemini API (Gemini 2.5 Flash):** Para la visión por computadora y la extracción de características/justificaciones.
* **Machine Learning:** Para la predicción de riesgo cardiovascular.


## 🚀 ¡Pruébalo!

1.  **Clona el repositorio:**
    ```bash
    git clone urldelrepo
    cd tu_repo
    ```
2.  **Configura tu entorno:**
    Asegúrate de tener Python instalado.  
    
3.  **Instala las librerías:**  
    * **scikit-learn**
    * **dotenv**
    * **google-genai**
    * **etc**

    
4.  **Configura tu clave de API de Gemini:**
    Crea un archivo `.env` en la raíz de tu proyecto y añade tu clave de API de Google Gemini:
    ```
    GOOGLE_API_KEY="TU_CLAVE_DE_API_DE_GOOGLE_GEMINI"
    ```
5.  **Coloca tu modelo entrenado:**
    Asegúrate de que tu modelo `best_model.pkl` esté en la ruta correcta (o ajusta la ruta en el código).
6.  **Prepara tu imagen:**
    Coloca una imagen `image1.jpg` en la carpeta `images/`. Hay una imagen en la carpeta images para que pruebes.

¡Observa cómo la IA analiza la imagen y te da una predicción y su razonamiento!

## 🧠 Reflexiones y Futuro

Este proyecto es una muestra del potencial inmenso de la IA en la salud y para cualquier otro campo. Podríamos expandirlo para:
* Integrar más características físicas o de comportamiento.
* Conectar con bases de datos de salud para validación.
* Desarrollar una interfaz de usuario más amigable.

La combinación de modelos multimodales (como Gemini) y el Machine Learning clásico abre puertas a aplicaciones que antes parecían ciencia ficción. ¡La IA no solo optimiza, sino que también innova y explica!

---

¡Explora el código, haz tus propias pruebas y sé parte de la revolución de la IA en la salud!
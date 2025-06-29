import streamlit as st
import os
import tempfile
import cohere
from dotenv import load_dotenv

from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import SystemMessagePromptTemplate

# --- 0. Configuración inicial ---
load_dotenv() 


st.set_page_config(layout="wide", page_title="Asesor de Optimización de CV con IA")

# --- Funciones de Carga y Procesamiento (Cacheables) ---

@st.cache_resource
def get_embeddings_model():
    """Crea y cachea el modelo de embeddings de Cohere."""
    return CohereEmbeddings(model="embed-v4.0") 

@st.cache_resource
def get_llm_models():
    """Crea y cachea los modelos LLM de Cohere."""
    llm_summarizer_and_chat = ChatCohere(model="command-r-plus", temperature=0.3)
    return llm_summarizer_and_chat

@st.cache_resource
def get_vector_store_and_retriever(pdf_path: str):
    """
    Carga el PDF, lo divide en chunks, crea el VectorStore y el Retriever.
    Se cachea para evitar reprocesar el PDF en cada interacción.
    """
    st.info(f"Cargando y procesando CV desde: {pdf_path}...")
    loader = PyMuPDFLoader(pdf_path) 
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50 
    )
    chunks = text_splitter.split_documents(documents)
    
    embeddings = get_embeddings_model()
    vector_db = Chroma.from_documents(chunks, embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3}) 
    st.success("CV procesado y listo.")
    return retriever

# --- Función para el resumen de la DPT (usando Cohere Client directamente) ---
def get_dpt_summary(long_dpt_text: str) -> str:
    co = cohere.ClientV2()

    system_message_content = """
    Eres un asistente experto en extracción de información clave.
    Tu tarea es resumir la siguiente Descripción de Puesto de Trabajo (DPT) larga en sus puntos más esenciales.
    Enfócate en las responsabilidades clave, requisitos obligatorios, habilidades técnicas y experiencia solicitada.
    El resumen debe ser conciso y no exceder los 200 tokens.
    """

    res = co.chat(
        model="command-a-03-2025",
        messages=[
            {"role": "system", "content": system_message_content},
            {
                "role": "user",
                "content": long_dpt_text,
            },
        ],  
    )
    return res.message.content[0].text 

# --- Función para crear el Prompt Personalizado (con historial de chat) ---
def create_cv_optimization_chat_prompt():
    """
    Crea un ChatPromptTemplate personalizado que incluye el historial de chat,
    la DPT, el contexto del CV y la pregunta actual del usuario.
    """
    system_template = """
    Eres un **asesor experto en selección de personal y optimización de CVs**.
    Tu tarea es analizar el CV de un candidato en el contexto de la descripción de un puesto específico y ofrecer **sugerencias detalladas, accionables y altamente relevantes** para adaptar el CV.
    Concéntrate en:
    - Palabras clave y terminología clave de la DPT.
    - Cómo reformular o enfatizar habilidades y experiencias del CV.
    - Posibles lagunas o información que falte en el CV.
    - Cuantificación de logros y resultados.
    Tu objetivo es maximizar las posibilidades del candidato de pasar el filtro inicial y captar la atención del reclutador.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    
    human_template = """
    Aquí está la **Descripción del Puesto de Trabajo (DPT)** que estamos usando para el análisis:
    ---
    {job_description}
    ---

    Aquí están las **secciones relevantes del CV** del candidato obtenidas del documento:
    ---
    {context_cv}
    ---

    Ahora, por favor, responde a la siguiente pregunta o solicitud:
    {question}
    """
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([
        system_message_prompt,
        MessagesPlaceholder(variable_name="chat_history"),
        human_message_prompt
    ])

    return chat_prompt

# --- Función para formatear los documentos recuperados ---
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# --- Configuración de la Interfaz de Streamlit ---

st.title("💡 Asesor de CV impulsado por IA")
st.markdown("Optimiza tu CV para cualquier puesto de trabajo con la ayuda de la Inteligencia Artificial.")

# Inicialización del estado de la sesión
# Se inicializa como cadena vacía por si acaso, pero la lógica de invocación la pasará directamente
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_processed_path" not in st.session_state:
    st.session_state.pdf_processed_path = None
if "dpt_summarized" not in st.session_state:
    st.session_state.dpt_summarized = "" 
if "retriever_obj" not in st.session_state:
    st.session_state.retriever_obj = None
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "last_dpt_summary_used" not in st.session_state: # <-- Nueva variable para guardar el resumen usado
    st.session_state.last_dpt_summary_used = ""

# --- Columna para la Entrada de Datos ---
with st.sidebar:
    st.header("1. Carga tu CV y DPT")

    uploaded_file = st.file_uploader("Sube tu CV en formato PDF", type="pdf")
    if uploaded_file and uploaded_file.name != (st.session_state.pdf_processed_path or "").split('/')[-1]:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            st.session_state.pdf_processed_path = tmp_file.name
        
        st.session_state.retriever_obj = get_vector_store_and_retriever(st.session_state.pdf_processed_path)
        st.success(f"CV '{uploaded_file.name}' cargado y procesado.")

    dpt_input = st.text_area(
        "Pega aquí la Descripción del Puesto de Trabajo (DPT)",
        height=300,
        placeholder="Ej: 'Buscamos un Ingeniero de Software con experiencia en Python, IA y ML...'"
    )

    if st.button("Generar Sugerencias de Optimización", type="primary"):
        if not st.session_state.pdf_processed_path:
            st.error("Por favor, sube tu CV en PDF primero.")
        elif not dpt_input:
            st.error("Por favor, introduce la Descripción del Puesto de Trabajo.")
        else:
            with st.spinner("Analizando DPT y CV para generar sugerencias..."):
                llm_model_for_chat = get_llm_models()
                
                # Generar el resumen de la DPT
                st.session_state.dpt_summarized = get_dpt_summary(dpt_input) 
                st.session_state.last_dpt_summary_used = st.session_state.dpt_summarized # <-- Guardar el resumen actual

                st.info("Resumen de la DPT:")
                st.markdown(f"```\n{st.session_state.dpt_summarized}\n```")

                retriever_obj = st.session_state.retriever_obj
                custom_chat_prompt = create_cv_optimization_chat_prompt()

                # Siempre crear la cadena si los componentes están listos
                if retriever_obj is not None: 
                    st.session_state.rag_chain = (
                        RunnablePassthrough.assign(
                            context_cv=lambda x: format_docs(retriever_obj.invoke(x["question"])),
                            # ¡CAMBIO CLAVE AQUÍ! job_description ahora se esperará como parte del input
                            # Ya no se accede a st.session_state.dpt_summarized dentro de la lambda de asignación
                        )
                        | custom_chat_prompt
                        | llm_model_for_chat
                        | StrOutputParser()
                    )

                    initial_query = "Genera las sugerencias de optimización para mi CV basándote en la DPT y el contexto del CV."
                    
                    st.session_state.messages = []
                    st.session_state.messages.append({"role": "user", "content": initial_query})

                    # ¡CAMBIO CLAVE AQUÍ! Pasar el resumen de la DPT directamente en la invocación
                    response = st.session_state.rag_chain.invoke({
                        "question": initial_query,
                        "chat_history": st.session_state.messages,
                        "job_description": st.session_state.last_dpt_summary_used # <-- ¡PÁSAME DIRECTO!
                    })
                    
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.success("Sugerencias generadas.")
                    st.rerun()
                else:
                    st.error("Hubo un problema al inicializar los componentes del CV. Intenta subir el CV de nuevo.")

# --- Sección Principal para el Chat ---
st.header("2. Tus Sugerencias y Conversación")

if st.session_state.messages:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("¿Alguna otra pregunta o necesitas más detalles sobre las sugerencias?"):
        if st.session_state.rag_chain: 
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            with st.spinner("Generando respuesta..."):
                # ¡CAMBIO CLAVE AQUÍ! Pasar el resumen de la DPT directamente en la invocación
                response = st.session_state.rag_chain.invoke({
                    "question": prompt,
                    "chat_history": st.session_state.messages,
                    "job_description": st.session_state.last_dpt_summary_used # <-- ¡PÁSAME DIRECTO!
                })
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.write(response)
        else:
            st.warning("Por favor, genera las sugerencias iniciales primero para iniciar el chat.")
else:
    st.info("Sube tu CV y pega la DPT en la barra lateral para empezar.")
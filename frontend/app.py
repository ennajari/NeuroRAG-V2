"""
Interface Streamlit pour NeuroRAG
"""
import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from ingestion.document_loader import document_loader
from ingestion.chunker import chunker
from knowledge.vector_store import vector_store
from agents.rag_agent import rag_agent
from config.settings import settings


st.set_page_config(
    page_title="NeuroRAG V2.0",
    page_icon="※",
    layout="wide"
)

st.title("NeuroRAG V2.0")
st.markdown("*Systeme RAG Intelligent avec Multi-Agents*")

# Sidebar
with st.sidebar:
    st.header("Gestion Documents")
    
    uploaded_file = st.file_uploader(
        "Uploader un document",
        type=['txt', 'pdf', 'docx'],
        help="Formats supportes: TXT, PDF, DOCX"
    )
    
    if uploaded_file:
        if st.button("Indexer Document"):
            with st.spinner("Traitement en cours..."):
                # Sauvegarder temporairement
                temp_path = settings.DOCUMENTS_DIR / uploaded_file.name
                with open(temp_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                # Charger et indexer
                doc = document_loader.load(str(temp_path))
                chunks = chunker.chunk_document(doc)
                ids = vector_store.add_documents(chunks)
                
                st.success(f"✓ Document indexe: {len(chunks)} chunks")
    
    st.divider()
    
    st.header("Statistiques")
    try:
        info = vector_store.get_collection_info()
        st.metric("Documents indexes", info['points_count'])
        st.metric("Status", info['status'])
    except:
        st.warning("Collection non initialisee")
    
    st.divider()
    
    if st.button("Reinitialiser"):
        try:
            vector_store.delete_collection()
            st.success("Collection supprimee")
            st.rerun()
        except:
            st.error("Erreur suppression")

# Main chat interface
st.header("Chat Interface")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.markdown(f"**Score: {source['score']:.3f}**")
                    st.text(source['preview'])
                    st.divider()

if prompt := st.chat_input("Posez votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Reflexion en cours..."):
            result = rag_agent.process({'query': prompt})
            
            st.markdown(result['answer'])
            
            if result['sources']:
                with st.expander("Sources"):
                    for source in result['sources']:
                        st.markdown(f"**Score: {source['score']:.3f}**")
                        st.text(source['preview'])
                        st.divider()
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": result['answer'],
            "sources": result['sources']
        })
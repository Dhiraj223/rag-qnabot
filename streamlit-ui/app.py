import streamlit as st
from ragqnabot.configs import PINECONE_API_KEY
from ragqnabot import DocumentLoader, DocumentSplitter, VectorStore, generate_answer, setup_pinecone, list_indexes
from pinecone import Pinecone
import os

def extract_text(response):
    if isinstance(response, list) and len(response) > 0:
        item = response[0]
        if hasattr(item, 'text'):
            return item.text
    return str(response)

def initialize_session_state():
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False
    if 'indexed' not in st.session_state:
        st.session_state.indexed = False
    if 'index' not in st.session_state:
        st.session_state.index = None
    if 'chunks' not in st.session_state:
        st.session_state.chunks = None
    if 'qna_mode' not in st.session_state:
        st.session_state.qna_mode = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def handle_file_upload():
    uploaded_file = st.file_uploader("Upload a document file", type=["txt", "pdf", "docx"])
    if uploaded_file is not None:
        with st.spinner("Processing your document..."):
            data_path = os.path.join("./data", uploaded_file.name)
            with open(data_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            loader = DocumentLoader(path=data_path)
            data = loader.load_data()

            splitter = DocumentSplitter(data=data)
            chunks = splitter.split_data()

            st.session_state.chunks = chunks
            st.session_state.file_uploaded = True
            st.success(f"File successfully uploaded and split into {len(chunks)} chunks!")

def handle_indexing():
    if st.session_state.file_uploaded:
        with st.expander("Index your document", expanded=not st.session_state.indexed):
            index_name = st.text_input("Enter a name for your index", key="index_name")
            index_button = st.button("Create Index", disabled=not index_name)
            
            if index_button and st.session_state.chunks:
                with st.spinner("Indexing document... This may take a few moments."):
                    try:
                        vecstore = VectorStore()
                        vecstore.add_texts(chunks=st.session_state.chunks)
                        vectors = vecstore.vectors
                        index = setup_pinecone(index_name=index_name, vectors=vectors)
                        st.session_state.index = index
                        st.session_state.indexed = True
                        st.session_state.qna_mode = True
                        st.success(f"Document successfully indexed as: {index_name}")
                    except Exception as e:
                        st.error(f"Error during indexing: {str(e)}")

def handle_index_selection():
    try:
        existing_indexes = list_indexes()
        existing_indexes = [str(index["name"]) for index in existing_indexes]
    except Exception as e:
        st.error(f"Error fetching existing indexes: {str(e)}")
        existing_indexes = []

    if existing_indexes:
        selected_index = st.selectbox("Select an existing index:", existing_indexes)
        if st.button("Use Selected Index"):
            try:
                pinecone = Pinecone(api_key=PINECONE_API_KEY)
                index = pinecone.Index(selected_index)
                st.session_state.index = index
                st.session_state.indexed = True
                st.session_state.qna_mode = True
                st.success(f"Using existing index: {selected_index}")
            except Exception as e:
                st.error(f"Error loading existing index: {str(e)}")
    else:
        st.info("No existing indexes found. Please upload a document to create a new index.")

def handle_qa_chat():
    if st.session_state.indexed and st.session_state.qna_mode:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Chat with your document")
        
        # Display chat history
        for i, (query, answer) in enumerate(st.session_state.chat_history):
            message(query, is_user=True, key=f"user_msg_{i}")
            st.markdown("<br>", unsafe_allow_html=True)
            message(answer, key=f"ai_msg_{i}")
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Chat input
        st.markdown("<br>", unsafe_allow_html=True)
        user_input = st.text_input("Ask a question about your document", key="user_input",  value="")
        if st.button("Send", key="send_button"):
            if user_input:
                with st.spinner("Thinking..."):
                    try:
                        vecstore_new = VectorStore()
                        retrieved_docs = vecstore_new.similarity_search(index=st.session_state.index, query=user_input, k=3)
                        if retrieved_docs:
                            answer = generate_answer(query=user_input, retrieved_docs=retrieved_docs)
                            response = extract_text(answer)
                            
                            # Add to chat history
                            st.session_state.chat_history.append((user_input, response))
                            
                            # Rerun to update the chat display
                            st.rerun()
                        else:
                            st.warning("No relevant information found in the document.")
                    except Exception as e:
                        st.error(f"Error during question answering: {str(e)}")
            else:
                st.warning("Please enter a question.")

def message(content, is_user=False, key=None):
    if is_user:
        st.markdown(f'<div style="text-align: right;"><span style="background-color: #25c5f1; color: white; padding: 5px 10px; border-radius: 15px;">{content}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align: left;"><span style="background-color: #f1f1f1; color: black; padding: 5px 10px; border-radius: 15px;">{content}</span></div>', unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Smart Document Q&A", layout="wide")
    st.title("📚 Smart Document Q&A System")

    initialize_session_state()

    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Choose a mode:", ["Upload & Index", "Use Existing Index", "Chat with Document"])

    if app_mode == "Upload & Index":
        st.header("📤 Upload and Index Your Document")
        handle_file_upload()
        handle_indexing()
    elif app_mode == "Use Existing Index":
        st.header("🔍 Select an Existing Index")
        handle_index_selection()
    elif app_mode == "Chat with Document":
        st.header("💬 Chat with Your Document")
        if st.session_state.indexed:
            handle_qa_chat()
        else:
            st.warning("Please upload and index a document or select an existing index before starting a chat.")

    st.sidebar.markdown("---")
    st.sidebar.info("This app allows you to upload documents, index them, and chat about their content using AI.")

if __name__ == "__main__":
    main()
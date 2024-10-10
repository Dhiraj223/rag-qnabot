import streamlit as st
from ragqnabot.configs import PINECONE_API_KEY
from ragqnabot import DocumentLoader, DocumentSplitter, VectorStore, generate_answer, setup_pinecone, list_indexes
from pinecone import Pinecone

def extract_text(response):
    if isinstance(response, list) and len(response) > 0:
        item = response[0]
        if hasattr(item, 'text'):
            return item.text
    return str(response)

def main():
    st.set_page_config(page_title="Document Q&A System", layout="wide")
    st.title("Document Q&A System")

    # Initialize session state variables
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

    # Index Selection
    if not st.session_state.qna_mode:
        st.write("### Select Index")
        try:
            existing_indexes = list_indexes()
            existing_indexes = [str(index["name"]) for index in existing_indexes]
        except Exception as e:
            st.error(f"Error fetching existing indexes: {str(e)}")
            existing_indexes = []

        index_option = st.radio(
            "Choose an option:",
            ("Use existing index", "Create new index")
        )

        if index_option == "Use existing index" and existing_indexes:
            selected_index = st.selectbox("Select an existing index:", existing_indexes)
            if st.button("Use Selected Index"):
                try:
                    # Load the existing index object, not just the name
                    pinecone = Pinecone(api_key=PINECONE_API_KEY)
                    index = pinecone.Index(selected_index)  # Load the Pinecone index object
                    st.session_state.index = index  # Store the actual index object
                    st.session_state.indexed = True
                    st.session_state.qna_mode = True
                    st.success(f"Using existing index: {selected_index}")
                except Exception as e:
                    st.error(f"Error loading existing index: {str(e)}")

        elif index_option == "Create new index" or not existing_indexes:
            st.session_state.file_uploaded = False
            st.session_state.indexed = False
            st.session_state.index = None

            # File Upload Section (only show if creating a new index)
            uploaded_file = st.file_uploader("Upload a document file", type=["txt", "pdf", "docx"])
            if uploaded_file is not None:
                data_path = f"./data/{uploaded_file.name}"
                with open(data_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Load the data using DocumentLoader
                loader = DocumentLoader(path=data_path)
                data = loader.load_data()

                # Split the data into chunks
                splitter = DocumentSplitter(data=data)
                chunks = splitter.split_data()

                st.session_state.chunks = chunks
                st.session_state.file_uploaded = True
                st.success(f"File successfully uploaded and split into {len(chunks)} chunks!")

            # Indexing Section
            if st.session_state.file_uploaded:
                st.write("### Indexing")
                index_name = st.text_input("Enter Index Name")
                index_button = st.button("Index Document", disabled=not index_name)
                
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
                            st.success(f"Document successfully indexed with name: {index_name}")
                        except Exception as e:
                            st.error(f"Error during indexing: {str(e)}")

    # Q&A Section
    if st.session_state.indexed and st.session_state.qna_mode:
        st.write("### Ask Questions")
        query = st.text_input("Ask a question based on the document")
        if st.button("Submit Question"):  # Only take input on button click
            if query:
                with st.spinner("Fetching answer..."):
                    try:
                        vecstore_new = VectorStore()
                        retrieved_docs = vecstore_new.similarity_search(index=st.session_state.index, query=query, k=3)
                        if retrieved_docs:
                            answer = generate_answer(query=query, retrieved_docs=retrieved_docs)
                            st.write("**Answer:**")
                            st.write(extract_text(answer))
                        else:
                            st.warning("No relevant documents found.")
                    except Exception as e:
                        st.error(f"Error during question answering: {str(e)}")

if __name__ == "__main__":
    main()

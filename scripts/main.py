from ragqnabot import DocumentLoader, DocumentSplitter, VectorStore, generate_answer, setup_pinecone


def main() :
    data_path = input("Enter Your Data Path : ")
    loader = DocumentLoader(path=data_path)
    data = loader.load_data()

    splitter = DocumentSplitter(data=data)
    chunks = splitter.split_data()

    vectstore = VectorStore()
    vectstore.add_texts(chunks=chunks)

    vectors = vectstore.vectors
    index_name = input("Enter Index Name : ")
    index = setup_pinecone(index_name, vectors)

    while True :
        query = input("Ask a Query or type 'Quit' to Exit : ")

        if query == "Quit" :
            break

        else :
            relevant_chunks = vectstore.similarity_search(index, query, k=3)

            answer = generate_answer(query, relevant_chunks)

            print(answer)

if __name__ == "__main__" :
    main()
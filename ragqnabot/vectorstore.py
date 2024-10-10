from sentence_transformers import SentenceTransformer
from typing import List, Dict, Union, Tuple

class VectorStore:
    """
    A class for storing, indexing, and retrieving text data using vector embeddings,
    optimized for Retrieval-Augmented Generation (RAG).
    """

    def __init__(self, embedding_model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the VectorStore.

        Args:
            embedding_model_name (str): The name of the sentence transformer model to use for embeddings.
        """
        self.vectors = []  # List of tuples (id, embedding, chunks)
        self.model = SentenceTransformer(embedding_model_name)

    def add_texts(self, chunks: List[Dict[str, Union[str, int]]]) -> None:
        """
        Add text chunks to the vector store.

        Args:
            chunks (List[Dict[str, Union[str, int]]]): A list of text chunks with their metadata.
        """
        for i, chunk in enumerate(chunks):
            embedding = self.model.encode(chunk['text'])
            metadata  = {
                "text" : chunk["text"]
            }
            self.vectors.append((str(i), embedding.tolist(), metadata))

    def similarity_search(self, index, query: str, k: int = 5) -> List[Tuple[Dict[str, Union[str, int]], float]]:
        """
        Perform a similarity search for the given query.

        Args:
            query (str): The search query.
            k (int): The number of top results to return.

        Returns:
            List[Tuple[Dict[str, Union[str, int]], float]]: A list of tuples containing the top-k similar chunks and their similarity scores.
        """
        query_embedding = self.model.encode(query)
        results = index.query(vector=query_embedding.tolist(), top_k=k)
        ids_to_fetch = [match['id'] for match in results['matches']]
        fetched_embeddings = index.fetch(ids=ids_to_fetch)
        fetched_chunks = [data.get("metadata") for id,data in fetched_embeddings["vectors"].items()]
        return [chunk for chunk in fetched_chunks]
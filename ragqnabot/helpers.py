from ragqnabot.configs import PINECONE_API_KEY
from pinecone import Pinecone, ServerlessSpec

def setup_pinecone(index_name, vectors, pinecone_api=PINECONE_API_KEY):
    """
    Set up a Pinecone index for storing and retrieving vector embeddings.

    Args:
        index_name (str): The name of the index to create or use.
        vectors (list): A list of vectors to be added to the index.
        pinecone_api (str): The API key for authenticating with Pinecone.

    Returns:
        Index: The initialized Pinecone index object for further operations.

    Raises:
        Exception: Raises an exception if there is an error during index creation or vector upsertion.

    This function initializes a Pinecone client with the provided API key, checks if the index already exists,
    creates it if necessary, and uploads the given vectors to the index.
    """
    pinecone = Pinecone(api_key=pinecone_api)
    
    try:
        # Check if the index already exists
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

        index = pinecone.Index(index_name)
        index.upsert(vectors=vectors)

        return index

    except Exception as e:
        raise Exception(f"An error occurred while setting up the Pinecone index: {e}")
    
def list_indexes(pinecone_api=PINECONE_API_KEY):
    pinecone = Pinecone(api_key=pinecone_api)
    indexes = pinecone.list_indexes()
    return indexes

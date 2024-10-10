import cohere
from typing import List, Dict
from ragqnabot.configs import COHERE_API_KEY

def generate_answer(query: str, retrieved_docs: List[Dict[str, str]], cohere_api: str = COHERE_API_KEY) -> str:
    """
    Generate an answer based on the query and retrieved documents.

    Args:
        query (str): The user's question.
        retrieved_docs (List[Dict[str, str]]): A list of retrieved relevant documents.
        cohere_api (str): The API key for Cohere.

    Returns:
        str: The generated answer or an error message.
    """
    try:
        co = cohere.ClientV2(cohere_api)
        context = "\n".join([doc['text'] for doc in retrieved_docs])
        prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
        response = co.chat(
            model="command-r-plus",
            messages = [
            {"role": "system", "content": "You are a helpful AI assistant that provides concise answers based on the provided context. Respond with only the answer to the question, without adding any extra explanation or text."},
            {"role": "user", "content": prompt},
            ]
        )

        return response.message.content

    except Exception as e:
        return f"An error occurred while generating the answer: {str(e)}"
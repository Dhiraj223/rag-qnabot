import os
from dotenv import load_dotenv

load_dotenv('.env')

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
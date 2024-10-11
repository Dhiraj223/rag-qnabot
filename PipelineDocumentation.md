# Document Processing Pipeline Documentation

## Overview

This document processing pipeline provides a comprehensive solution for loading, splitting, storing, and retrieving documents efficiently using vector embeddings. It also integrates with an external API (Cohere) for generating answers based on user queries. The pipeline is designed to support retrieval-augmented generation (RAG) workflows and can handle various document formats.

## Components

### 1. DocumentLoader

**Purpose:** Loads data from various file formats or URLs.

**Key Features:**
- Supports multiple file formats: PDF, DOCX, HTML, TXT, CSV, Excel, and images (via OCR)
- Handles web page loading from URLs
- Provides a unified interface for data loading regardless of the source

**Main Methods:**
- `load_data()`: Loads and returns the content of the specified file or URL
- Various format-specific loading methods (e.g., `_load_pdf()`, `_load_docx()`, etc.)

**Usage Example:**
```python
loader = DocumentLoader(path="document.pdf")
data = loader.load_data()
```

### 2. DocumentSplitter

**Purpose:** Splits large text data into smaller, manageable chunks for processing and retrieval.

**Key Features:**
- Configurable chunk size and overlap
- Ensures context preservation through overlapping chunks

**Main Methods:**
- `split_data()`: Splits the input text into a list of overlapping chunks

**Usage Example:**
```python
splitter = DocumentSplitter(data, chunk_size=1000, overlap=200)
chunks = splitter.split_data()
```

### 3. VectorStore

**Purpose:** Stores, indexes, and retrieves text chunks using vector embeddings for efficient similarity search.

**Key Features:**
- Uses SentenceTransformer models for generating embeddings
- Supports similarity search for retrieving relevant document chunks

**Main Methods:**
- `add_texts()`: Adds text chunks to the vector store and generates embeddings
- `similarity_search()`: Performs similarity search to retrieve relevant chunks for a given query

**Usage Example:**
```python
vecstore = VectorStore()
vecstore.add_texts(chunks)
relevant_chunks = vecstore.similarity_search(index, query, k=5)
```

### 4. Pinecone Integration

**Purpose:** Provides cloud-based vector storage and indexing for efficient retrieval.

**Key Features:**
- Creates and manages vector indexes in the cloud
- Supports efficient similarity search at scale

**Usage Example:**
```python
pinecone = Pinecone(api_key=pinecone_api)
index = pinecone.Index(index_name)
index.upsert(vectors=vectors)
```

### 5. Answer Generation

**Purpose:** Generates concise answers to user queries based on retrieved relevant documents.

**Key Components:**
- `generate_answer()` function: Processes retrieved documents and generates an answer
- `ans_query()` function: Orchestrates the query process, including document retrieval and answer generation

**Usage Example:**
```python
response = ans_query()
print(response)
```

## Workflow

1. Load a document using `DocumentLoader`
2. Split the document into chunks with `DocumentSplitter`
3. Store and index the chunks using `VectorStore` and Pinecone
4. Process user queries and generate answers using the `ans_query()` function

## Dependencies

- Python Libraries: requests, beautifulsoup4, PyPDF2, docx, pytesseract, chardet, pandas, SentenceTransformer, cohere
- External Services: Cohere API, Pinecone

## Notes

- The pipeline is optimized for retrieval-augmented generation (RAG) workflows
- It can handle various document formats and perform similarity-based document retrieval
- The system uses the `cohere.ClientV2` API for generating concise answers from retrieved context

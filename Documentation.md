# DocumentLoader Class

The `DocumentLoader` class is designed to load data from various file formats, including PDFs, DOCX, HTML, CSV, Excel, text files, and images, as well as web pages. It simplifies the process of loading and extracting data from files or URLs, making it suitable for different use cases.

## Libraries Used

The class makes use of the following Python libraries:

- `os`: For handling file paths and extensions.
- `docx`: For reading DOCX files.
- `PyPDF2`: For reading PDF files.
- `chardet`: For detecting file encoding.
- `requests`: For fetching web pages.
- `pytesseract`: For extracting text from images using Optical Character Recognition (OCR).
- `pandas`: For handling CSV and Excel files.
- `PIL`: For opening and processing image files.
- `BeautifulSoup`: For parsing HTML content.
- `typing`: For type annotations.
- `urllib.parse`: For checking if the input path is a valid URL.

## Class: DocumentLoader

### Constructor: `__init__(self, path: str)`

Initializes the `DocumentLoader` object.

- **Parameters**:
  - `path` (str): The path to the file to be loaded or a URL.

- **Attributes**:
  - `self.path`: Stores the file path or URL.
  - `self.data`: Holds the loaded data.

### Method: `load_data(self) -> Union[str, Dict[str, Any]]`

Loads the data from the file or URL based on its format.

- **Returns**:
  - `Union[str, Dict[str, Any]]`: The loaded data as a string or dictionary.

- **Raises**:
  - `ValueError`: If the file format is unsupported or the URL is invalid.
  - `IOError`: If there's an error reading the file or loading the web page.

### Private Method: `_is_url(self, path: str) -> bool`

Checks if the given path is a URL.

- **Parameters**:
  - `path` (str): The path or URL to be checked.

- **Returns**:
  - `bool`: `True` if the path is a valid URL, otherwise `False`.

### Private Method: `_load_web_page(self, url: str) -> str`

Fetches and loads text from a web page.

- **Parameters**:
  - `url` (str): The URL of the web page.

- **Returns**:
  - `str`: The text content of the web page.

- **Raises**:
  - `ValueError`: If the web page couldn't be loaded.

### Private Method: `_load_pdf(self) -> str`

Loads text from a PDF file.

- **Returns**:
  - `str`: The extracted text from the PDF.

- **Raises**:
  - `IOError`: If there's an error reading the PDF file.

### Private Method: `_load_docx(self) -> str`

Loads text from a DOCX file.

- **Returns**:
  - `str`: The extracted text from the DOCX file.

- **Raises**:
  - `IOError`: If there's an error reading the DOCX file.

### Private Method: `_load_html(self) -> str`

Loads text from an HTML file.

- **Returns**:
  - `str`: The extracted text from the HTML file.

- **Raises**:
  - `IOError`: If there's an error reading the HTML file.

### Private Method: `_load_txt(self) -> str`

Loads text from a TXT or Markdown file.

- **Returns**:
  - `str`: The extracted text from the TXT or Markdown file.

- **Raises**:
  - `IOError`: If there's an error reading the text file.

### Private Method: `_load_csv(self) -> str`

Loads data from a CSV file and converts it to a string.

- **Returns**:
  - `str`: The data in the CSV file formatted as a string.

- **Raises**:
  - `IOError`: If there's an error reading the CSV file.

### Private Method: `_load_excel(self) -> str`

Loads data from an Excel file and converts it to a string.

- **Returns**:
  - `str`: The data in the Excel file formatted as a string.

- **Raises**:
  - `IOError`: If there's an error reading the Excel file.

### Private Method: `_load_image(self) -> str`

Uses Optical Character Recognition (OCR) to extract text from an image file.

- **Returns**:
  - `str`: The extracted text from the image.

- **Raises**:
  - `IOError`: If there's an error reading the image file.

## Supported File Formats

- **PDF**: `.pdf`
- **DOCX**: `.docx`
- **HTML/HTM**: `.html`, `.htm`
- **Text/Markdown**: `.txt`, `.md`
- **CSV**: `.csv`
- **Excel**: `.xls`, `.xlsx`
- **Image**: `.jpg`, `.jpeg`, `.png`

## Example Usage

```python
# Initialize the DocumentLoader with a file path
doc_loader = DocumentLoader('sample.pdf')

# Load data from the file
data = doc_loader.load_data()

# Print the loaded data
print(data)
```

# DocumentSplitter Class

The `DocumentSplitter` class is designed to split large blocks of text data into smaller chunks with optional overlap and the ability to track the starting index of each chunk. This is useful for processing large text files or documents in smaller, manageable sections.

## Class: DocumentSplitter

### Constructor: `__init__(self, data: str, chunk_size: int = 1000, overlap: int = 200, add_start_index: bool = True)`

Initializes the `DocumentSplitter` object.

- **Parameters**:
  - `data` (str): The text data to be split.
  - `chunk_size` (int): The number of characters in each chunk. Default is 1000.
  - `overlap` (int): The number of characters to overlap between consecutive chunks. Default is 200.
  - `add_start_index` (bool): Whether to include the starting index of each chunk in the output. Default is `True`.

- **Attributes**:
  - `self.data`: Stores the text data.
  - `self.chunk_size`: Stores the size of each chunk.
  - `self.overlap`: Stores the number of overlapping characters between chunks.
  - `self.add_start_index`: Determines whether to include the start index in the output.

### Method: `split_data(self) -> List[str]`

Splits the input data into smaller chunks based on the specified `chunk_size` and `overlap`. Optionally, it can include the starting index of each chunk.

- **Returns**:
  - `List[Union[str, Dict[str, Union[str, int]]]]`: 
    - If `add_start_index` is `True`: Returns a list of dictionaries, each containing the chunk text and its start index.
    - If `add_start_index` is `False`: Returns a list of plain text chunks.

- **Process**:
  - The method iterates over the input text, splitting it into smaller chunks of `chunk_size` characters.
  - Each chunk can overlap with the next by the number of characters specified in the `overlap` parameter.
  - The starting index of each chunk is tracked and included in the output if `add_start_index` is `True`.

### Example Usage

```python
# Example text data
data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

# Initialize the DocumentSplitter
splitter = DocumentSplitter(data, chunk_size=50, overlap=10, add_start_index=True)

# Split the data
chunks = splitter.split_data()

# Print the chunks
for chunk in chunks:
    print(chunk)
```

# VectorStore Class

The `VectorStore` class provides a way to store, index, and retrieve text data using vector embeddings. It is particularly useful in tasks like **Retrieval-Augmented Generation (RAG)**, where text embeddings are used to retrieve relevant chunks of data based on a query.

## Class: VectorStore

### Constructor: `__init__(self, embedding_model_name: str = 'all-MiniLM-L6-v2')`

Initializes the `VectorStore` object.

- **Parameters**:
  - `embedding_model_name` (str): The name of the pre-trained model from `SentenceTransformer` to use for creating embeddings. Default is `'all-MiniLM-L6-v2'`.

- **Attributes**:
  - `self.vectors`: A list to store tuples consisting of an ID, the text embedding, and chunk metadata.
  - `self.model`: The sentence transformer model for generating embeddings.

### Method: `add_texts(self, chunks: List[Dict[str, Union[str, int]]]) -> None`

Adds chunks of text to the vector store. Each chunk is transformed into its corresponding embedding using the pre-trained model.

- **Parameters**:
  - `chunks` (List[Dict[str, Union[str, int]]]): A list of dictionaries, where each dictionary contains the text chunk and optional metadata (such as start index).

- **Process**:
  - Iterates through the provided text chunks.
  - Converts each chunk of text into its corresponding vector embedding using the pre-trained model.
  - Stores the vector embedding, its unique ID, and the text metadata (which includes the original chunk of text).

### Method: `similarity_search(self, index, query: str, k: int = 5) -> List[Tuple[Dict[str, Union[str, int]], float]]`

Performs a similarity search by comparing a query with the stored text embeddings and returning the top-k most similar results.

- **Parameters**:
  - `index`: The vector index where the embeddings are stored. This is required to perform the query.
  - `query` (str): The input text query to find similar chunks.
  - `k` (int): The number of top similar chunks to return. Default is `5`.

- **Returns**:
  - `List[Tuple[Dict[str, Union[str, int]], float]]`: 
    - A list of tuples, where each tuple contains the metadata of the similar chunk and its similarity score.

- **Process**:
  - Encodes the input query into a vector embedding using the same pre-trained model.
  - Performs a similarity search using the vector index and returns the top `k` most similar chunks.
  - Fetches the metadata (which contains the text) of each similar chunk using its ID.

### Example Usage

```python
# Example text chunks
chunks = [
    {"text": "The quick brown fox jumps over the lazy dog."},
    {"text": "Artificial intelligence is transforming industries."},
    {"text": "Data science and machine learning are closely related fields."}
]

# Initialize the VectorStore
store = VectorStore()

# Add the text chunks to the vector store
store.add_texts(chunks)

# Perform a similarity search
top_results = store.similarity_search(index, query="Machine learning")

# Print the top results
for result in top_results:
    print(result)
```
### Sample Output
```python
[
    {"text": "Data science and machine learning are closely related fields."},
    {"text": "Artificial intelligence is transforming industries."}
]
```

### Parameters in Detail

- **embedding_model_name**: This is the name of the pre-trained transformer model that will generate vector embeddings from the text chunks. `all-MiniLM-L6-v2` is a commonly used model known for its efficiency and accuracy in generating meaningful text embeddings.

- **chunks**: Each chunk contains a portion of text that will be embedded and added to the vector store. These can represent sentences, paragraphs, or any textual data that requires retrieval.

- **query**: A textual query used to search for similar chunks. The query is converted to a vector embedding and compared with the stored chunks to find the most similar ones.

### Notes

- **RAG (Retrieval-Augmented Generation)**: This class is optimized for RAG tasks, where you retrieve relevant information (chunks) using vector embeddings and then use the retrieved data to generate answers or enhance models.
- The embeddings are stored in a `vectors` list, which can be used in various machine learning or search-based applications.
- The `SentenceTransformer` library is used to generate meaningful embeddings of the text for efficient similarity searches.


## `generate_answer`

This function generates an answer based on a user's query and a set of retrieved documents using the Cohere API.

### Arguments

- **`query`** (`str`):  
  The user's question or query.

- **`retrieved_docs`** (`List[Dict[str, str]]`):  
  A list of dictionaries containing relevant documents. Each dictionary should have at least a `'text'` key that holds the content of the document.

- **`cohere_api`** (`str`, optional):  
  The API key for accessing the Cohere service. If not provided, the default API key from the `COHERE_API_KEY` configuration will be used.

### Returns

- **`str`**:  
  The generated answer to the query based on the retrieved documents. If an error occurs during the process, an error message is returned.

### Example Usage

```python
retrieved_docs = [
    {"text": "Data science involves using algorithms to analyze data."},
    {"text": "Machine learning is a subset of artificial intelligence."}
]

query = "What is data science?"

answer = generate_answer(query, retrieved_docs)
print(answer)
```

### Notes

- **Cohere API**:  
  This function uses the Cohere API's chat feature with the `"command-r-plus"` model to generate answers based on the provided context.

- **Context Construction**:  
  The text from the retrieved documents is combined into a single string to provide context for generating the answer.

- **Error Handling**:  
  If the function encounters an error during API communication, it returns a descriptive error message.

## Pinecone Setup Functions

### `setup_pinecone(index_name: str, vectors: list, pinecone_api: str = PINECONE_API_KEY) -> Index`

Set up a Pinecone index for storing and retrieving vector embeddings.

#### Arguments:
- **`index_name` (str)**: The name of the index to create or use.
- **`vectors` (list)**: A list of vectors to be added to the index.
- **`pinecone_api` (str)**: The API key for authenticating with Pinecone.

#### Returns:
- **`Index`**: The initialized Pinecone index object for further operations.

#### Raises:
- **`Exception`**: Raises an exception if there is an error during index creation or vector upsertion.

#### Description:
This function initializes a Pinecone client with the provided API key, checks if the index already exists, creates it if necessary, and uploads the given vectors to the index.

---

### `list_indexes(pinecone_api: str = PINECONE_API_KEY) -> list`

List all existing Pinecone indexes.

#### Arguments:
- **`pinecone_api` (str)**: The API key for authenticating with Pinecone.

#### Returns:
- **`list`**: A list of index names.

#### Description:
This function initializes a Pinecone client with the provided API key and retrieves the names of all existing indexes.









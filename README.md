# Cloning the Repository and Running the Streamlit App

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Git
- Python 3.7 or higher
- pip (Python package installer)

## Step 1: Clone the Repository

1. Open a terminal or command prompt.
2. Navigate to the directory where you want to clone the repository.
3. Run the following command:
   ```
   git clone https://github.com/Dhiraj223/rag-qnabot.git
   ```
4. Navigate into the cloned repository:
   ```
   cd rag-qnabot
   ```

## Step 2: Set Up a Virtual Environment (Optional but Recommended)

1. Create a virtual environment:
   ```
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

## Step 3: Install Dependencies

Install the required packages using pip:
```
pip install -r requirements.txt
pip install -e .
```

## Step 4: Set Up Environment Variables

1. Create a `.env` file in the root directory of the project.
2. Add the following lines to the file:
   ```
   PINECONE_API_KEY=your_pinecone_api_key
   COHERE_API_KEY=your_cohere_Api_key
   ```
   Replace `your_pinecone_api_key` and `your_cohere_api_key` with your actual Pinecone and Cohere API keys.

## Step 5: Run the Streamlit App

1. Ensure you're in the project's root directory.
2. Run the following command:
   ```
   streamlit run streamlit-ui\app.py
   ```

3. Streamlit will start the app and provide you with a local URL (usually `http://localhost:8501`). It may also provide a network URL.

4. Open the provided URL in your web browser to use the Document Q&A System.

## User Guide

For detailed instructions on how to use this application, please refer to our [User Guide](USER_GUIDE.md).

## Troubleshooting

- If you encounter any "Module not found" errors, make sure you've activated your virtual environment and installed all dependencies correctly.
- If you have issues with Pinecone, ensure your API key is correctly set in the `.env` file and that you have an active Pinecone account.


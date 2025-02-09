## Overview
This web application enables users to upload PDF and DOCX documents and ask questions based on their content. It processes documents by extracting text, generating embeddings, and delivering relevant answers through AI-powered search.

## Features
- **Upload Document:** Upload a PDF or DOCX file to analyze its content.
- **Ask Question:** Ask questions about the uploaded document and receive answers based on the content.
- **Show Embeddings:** View and analyze the embeddings data of the document content.

## Technologies Used
- **Backend:** Flask
- **Frontend:** Streamlit
- **Embeddings and Models:** Custom model selection and embedding functions
- **Database:** Custom database migrations and functions
- **Environment Variables:** Managed using `dotenv`

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/qa-with-pdf.git
    cd qa-with-pdf
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Setup environment variables:**
    - Create a `.env` file in the root directory of the project.
    - Add the following variables:
    ```env
    UPLOAD_FOLDER=./uploads
    HOME_BG_IMAGE=./images/home_bg.jpg
    UPLOAD_DOCUMENT_BG_IMAGE=./images/upload_document_bg.jpg
    ASK_QUESTION_BG_IMAGE=./images/ask_question_bg.jpg
    SHOW_EMBEDDING_BG_IMAGE=./images/show_embedding_bg.jpg
    ```

5. **Ensure the upload folder exists:**
    ```sh
    mkdir -p ./uploads
    ```

### Running the Application

1. **Start the Flask backend:**
    ```sh
    python app.py
    ```

2. **Start the Streamlit frontend:**
    ```sh
    streamlit run st_app.py
    ```

3. **Access the application:**
    - Backend API: http://127.0.0.1:5000
    - Frontend UI: http://localhost:8501

## Usage

### Upload Document
1. Navigate to the "Upload Document" page.
2. Upload a PDF or DOCX file.
3. Click the "Upload PDF" button to upload and process the document.

### Ask Question
1. Navigate to the "Ask Question" page.
2. Enter your question in the input field.
3. Click the "Get Answer" button to receive an answer based on the uploaded document's content.

### Show Embeddings
1. Navigate to the "Show Embeddings" page.
2. Click the "Show Embeddings" button to display the embeddings data.

import streamlit as st
import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()


# Function for saving uploaded documents
def save_uploadedfile(uploaded_file):
    try:
        file_path = os.path.join(os.getenv("UPLOAD_FOLDER"), uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())
        return file_path
    except Exception as e:
        st.error(f"Error saving uploaded file: {e}")
        return None

# Function for uploading documents
def upload_file(file_path, uploaded_file):
    url = "http://127.0.0.1:5000/file_upload"
    file_type = 'application/pdf' if uploaded_file.type == 'application/pdf' else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    files = [
        ('file', (uploaded_file.name, open(file_path, 'rb'), file_type))
    ]
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        st.success(response.text)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while uploading the file: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

# Function for asking questions
def ask_question(question):
    url = 'http://127.0.0.1:5000/ask_question'
    data = {"question": question}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json().get("answer", "No answer available")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while asking the question: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

# Function for getting embeddings
def get_embeddings():
    url = 'http://127.0.0.1:5000/get_embeddings'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while getting embeddings: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

# Function for getting base64 encoded image
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None
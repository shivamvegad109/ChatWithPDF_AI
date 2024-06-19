from st_fn import *
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Initialize session state if not already done
if 'responses' not in st.session_state:
    st.session_state.responses = {}

def main():
    st.set_page_config(page_title="Q & A with PDF 📄")

    st.markdown(
        """
        <style>
        .stApp {
            background-size: cover;
        }
        .st-bp {
            display: flex;
            justify-content: flex-end;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Background images for different pages
    background_images = {
        "🏠 Home": os.getenv("HOME_BG_IMAGE"),
        "📂 Upload Document": os.getenv("UPLOAD_DOCUMENT_BG_IMAGE"),
        "❓ Ask Question": os.getenv("ASK_QUESTION_BG_IMAGE"),
        "🔍 Show Embeddings": os.getenv("SHOW_EMBEDDING_BG_IMAGE"),
    }

    st.sidebar.title("Navigation 🚀")
    page = st.sidebar.radio("Select Page", options=["🏠 Home", "📂 Upload Document", "❓ Ask Question", "🔍 Show Embeddings"], index=0)
    uploaded_file = []

    if page == "🏠 Home":
        image_path = background_images[page]
        base64_image = get_base64_image(image_path)

        if base64_image:
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("data:image/jpeg;base64,{base64_image}");
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

        col1, col2 = st.columns([2, 1])
        with col1:
            st.title("Q & A with PDF 📄")
            st.markdown("### How to Use:")
            st.markdown(
                """
                Welcome to Q&A with PDF! Upload your document, ask questions, and explore embeddings.

                This tool helps you analyze and interact with the content of your documents in an easy and efficient way.

                - **📂 Upload Document:** Upload a PDF or DOCX file to analyze.
                - **❓ Ask Question:** Ask questions related to the document content.
                - **🔍 Show Embeddings:** View embeddings data for deeper analysis.
                """
            )
        with col2:
            st.write(" ")

    elif page == "📂 Upload Document":
        image_path = background_images[page]
        base64_image = get_base64_image(image_path)

        if base64_image:
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("data:image/jpeg;base64,{base64_image}");
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

        st.markdown("## Upload PDF 📜")
        uploaded_file = st.file_uploader('Upload a file', type=["pdf", "docx"])

        if uploaded_file is not None:
            file_path = save_uploadedfile(uploaded_file)

            if file_path and st.button("Upload PDF 🚀"):
                with st.spinner("Uploading"):
                    message = upload_file(file_path, uploaded_file)
                    if message:
                        st.success(message)
                        st.session_state.responses['upload_document'] = message
                        st.rerun()
        else:
            st.write("Please upload a file to proceed.")

        if 'upload_document' in st.session_state.responses:
            st.write("Stored response:", st.session_state.responses['upload_document'])

    elif page == "❓ Ask Question":
        image_path = background_images[page]
        base64_image = get_base64_image(image_path)

        if base64_image:
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("data:image/jpeg;base64,{base64_image}");
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(" ")
        with col2:
            st.markdown("## Ask a Question ❓")
            question = st.text_input("Enter your question:")

            if st.button("Get Answer 🪄"):
                with st.spinner("generating"):
                    if question:
                        answer = ask_question(question)
                        if answer:
                            st.session_state.responses['ask_question'] = answer
                            st.rerun()
                    else:
                        st.error("Please enter a question.")

            if 'ask_question' in st.session_state.responses:
                st.write("Stored response:", st.session_state.responses['ask_question'])

    elif page == "🔍 Show Embeddings":
        image_path = background_images[page]
        base64_image = get_base64_image(image_path)

        if base64_image:
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("data:image/jpeg;base64,{base64_image}");
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

        col1, col2 = st.columns([1, 10])
        with col1:
            st.write(" ")
        with col2:
            st.markdown("## Embeddings Data")
            if st.button("Show Embeddings 📊"):
                embeddings = get_embeddings()
                if embeddings:
                    df = pd.DataFrame(embeddings)
                    st.session_state.responses['show_embeddings'] = df
                    st.rerun()
                else:
                    st.error("No embeddings to display.")

            if 'show_embeddings' in st.session_state.responses:
                st.write("Stored response:")
                st.dataframe(st.session_state.responses['show_embeddings'])

if __name__ == "__main__":
    main()
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
import os
import faiss
import glob

load_dotenv()

# Function to load PDF and create retriever
def load_data(embeddings, file_path):
    try:
        # Define the index path
        filename = os.path.basename(file_path).split(".")[0]
        index_dir = os.path.join(os.getenv('FAISS_INDEX_PATH'), filename)
        index_path = os.path.join(index_dir, 'index')

        # Check if the FAISS index already exists
        if os.path.exists(index_path + ".faiss") and os.path.exists(index_path + ".pkl"):
            print(f"Loading existing FAISS index from {index_dir}")
            new_db = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
        else:
            # Load File
            loader = PyPDFLoader(file_path)
            docs = loader.load()

            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            documents = text_splitter.split_documents(docs)

            # Convert into embedding
            db = FAISS.from_documents(documents, embedding=embeddings)

            # Ensure the directory exists
            os.makedirs(index_dir, exist_ok=True)

            # Save embeddings into FAISS database
            db.save_local(index_dir)
            new_db = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)

        # Set the retriever
        retriever = new_db.as_retriever()
        return retriever

    except Exception as e:
        print(f"Error in load_data: {e}")
        return None

# Function to get all embeddings from the FAISS index files
def load_embeddings():
    try:
        index_dir = os.getenv('INDEX_DIR')
        index_paths = glob.glob(os.path.join(index_dir, '**', 'index.faiss'), recursive=True)
        if not index_paths:
            return [{"error": "No FAISS index files found"}]
        
        all_embeddings = []
        for index_path in index_paths:
            try:
                if not os.path.exists(index_path):
                    continue
                
                new_db = faiss.read_index(index_path)
                embeddings_list = new_db.reconstruct_n(0, new_db.ntotal)
                filename = os.path.basename(os.path.dirname(index_path))
                for i, emb in enumerate(embeddings_list):
                    all_embeddings.append({
                        "filename": filename,
                        "index_vector": i,
                        "data": emb.tolist()
                    })
            except Exception as e:
                print(f"Error reading index {index_path}: {e}")
                continue
        
        if not all_embeddings:
            return [{"error": "No embeddings found in any FAISS index"}]
        
        return all_embeddings
    except Exception as e:
        print(f"Error in load_embeddings: {e}")
        return [{"error": "Error in loading embeddings"}]

# Function to load model and embeddings
def model_selection_get_embed():
    try:
        llm = Ollama(model=os.getenv('OLLAMA_MODEL'), verbose=True)
        embeddings = HuggingFaceEmbeddings(model_name=os.getenv('EMBED_MODEL'))
        return llm, embeddings
    except Exception as e:
        print(f"Error in model_selection_get_embed: {e}")
        return None, None

# Function to generate response using prompt template
def prompt_template(llm, retriever, question):
    try:
        prompt = ChatPromptTemplate.from_template("""
            Answer the following question based only on the provided context. 
            Think step by step before providing a detailed answer. 
            I will tip you $1000 if the user finds the answer helpful. 
            <context>
            {context}
            </context>
            Question: {input}""")
        
        document_chain = create_stuff_documents_chain(llm, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        response = retrieval_chain.invoke({'input': question})
        return response['answer']
    except Exception as e:
        print(f"Error in prompt_template: {e}")
        return None

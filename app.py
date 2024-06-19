from flask import Flask, request, jsonify
from flask_cors import CORS
from functions import *
from database_connection.migrations import *
from dotenv import load_dotenv
import os 

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

@app.route('/file_upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            global retriever, llm, embeddings, file_name
            file = request.files['file']
            file_name = file.filename
            file_path = os.path.join(os.getenv('UPLOAD_FOLDER'), file_name)
            if not file_name:
                raise ValueError("No file name provided")
            llm, embeddings = model_selection_get_embed()
            retriever = load_data(embeddings, file_path)
            return jsonify(f"{file_name} uploaded successfully"), 200

        except Exception as e:
            return str(e), 500
        
@app.route('/ask_question', methods=['POST'])
def ask_question():
    if request.method == 'POST':
        try:
            global retriever, llm, file_name
            data = request.get_json()
            question = data['question']
            if not question:
                return jsonify({"error": "No question provided"}), 400

            if retriever is None:
                return jsonify({"error": "No document uploaded"}), 400

            answer = prompt_template(llm, retriever, question)
            message = insert_into_qa(question, answer, file_name)
            return jsonify({"answer":answer,
                            "message": message}), 200
        
        except Exception as e:
            return str(e), 500


@app.route('/get_embeddings', methods=['GET'])
def get_embeddings():
    try:
        all_embeddings = load_embeddings()
        return jsonify(all_embeddings), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000 , debug=False)
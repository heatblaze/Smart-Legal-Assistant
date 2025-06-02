from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from transformers import pipeline
from models import db, Feedback

from services.nlp import summarize_text, answer_question
from services.nlp import (
    extract_clauses,
    detect_risks,
    extract_entities,
    compare_to_template,
    semantic_search
)

import os

app = Flask(__name__)

# --- MySQL Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myuser:Alpha%40123@localhost/legal_assistant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

db = SQLAlchemy(app)

# --- Upload folder and allowed extensions ---
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Hugging Face Pipelines ---
summarizer = pipeline("summarization", model="google/flan-t5-large")
qa_pipeline = pipeline("question-answering", model="nlpaueb/legal-bert-base-uncased")

# --- Database Model ---
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)

# --- Helper function ---
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Routes ---

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Read content from file
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        # Save to database
        doc = Document(filename=filename, content=content)
        db.session.add(doc)
        db.session.commit()
        return jsonify({'message': 'File uploaded and saved to DB', 'filename': filename, 'doc_id': doc.id}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
    return jsonify({"summary": summary})

@app.route('/qa', methods=['POST'])
def qa():
    data = request.get_json()
    question = data.get("question", "")
    context = data.get("context", "")
    if not question or not context:
        return jsonify({"error": "Please provide question and context"}), 400
    result = qa_pipeline(question=question, context=context)
    return jsonify({"answer": result['answer'], "score": result['score']})

@app.route('/')
def index():
    return "Backend is running with MySQL and Hugging Face NLP!"

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    doc_id = data.get("doc_id")
    user_feedback = data.get("user_feedback")
    rating = data.get("rating")
    fb = Feedback(doc_id=doc_id, user_feedback=user_feedback, rating=rating)
    db.session.add(fb)
    db.session.commit()
    return jsonify({"message": "Feedback saved!"})

@app.route('/extract_clauses', methods=['POST'])
def extract_clauses_route():
    data = request.get_json()
    text = data.get("text", "")
    clauses = extract_clauses(text)
    return jsonify(clauses)

@app.route('/detect_risks', methods=['POST'])
def detect_risks_route():
    data = request.get_json()
    clauses = data.get("clauses", {})
    risks = detect_risks(clauses)
    return jsonify({"risks": risks})

@app.route('/entities', methods=['POST'])
def entities_route():
    data = request.get_json()
    text = data.get("text", "")
    entities = extract_entities(text)
    return jsonify({"entities": entities})

@app.route('/compare_template', methods=['POST'])
def compare_template_route():
    data = request.get_json()
    clauses = data.get("clauses", {})
    template_clauses = data.get("template_clauses", {})
    deviations = compare_to_template(clauses, template_clauses)
    return jsonify({"deviations": deviations})

@app.route('/semantic_search', methods=['POST'])
def semantic_search_route():
    data = request.get_json()
    query = data.get("query", "")
    clause_texts = data.get("clause_texts", [])
    match, score = semantic_search(query, clause_texts)
    return jsonify({"best_match": match, "score": score})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

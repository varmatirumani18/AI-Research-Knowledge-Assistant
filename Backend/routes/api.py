import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from database.db import db
from services.document_processor import DocumentProcessor
from services.rag_service import RAGService
from services.classifier_service import DocumentClassifier

api_bp = Blueprint('api', __name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'classifier.h5')
classifier = DocumentClassifier(MODEL_PATH)

@api_bp.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file attached"}), 400
    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Only PDF files are supported"}), 400

    filename = secure_filename(file.filename)
    upload_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    text, pages, chunks = DocumentProcessor.process_pdf(filepath)
    doc = db.add_document(filename, text, pages, chunks)

    return jsonify({
        "message": f"Document '{filename}' successfully ingested and indexed.",
        "doc_id": doc["id"],
        "total_pages": doc["total_pages"],
        "total_chunks": doc["total_chunks"]
    }), 200

@api_bp.route('/documents', methods=['GET'])
def list_docs():
    return jsonify({"documents": db.list_documents()}), 200

@api_bp.route('/documents/<doc_id>', methods=['DELETE'])
def delete_doc(doc_id):
    if db.delete_document(doc_id):
        return jsonify({"message": "Document removed successfully"}), 200
    return jsonify({"error": "Document not found"}), 404

@api_bp.route('/query', methods=['POST'])
def query():
    data = request.json or {}
    question = data.get("question", "")
    mode = data.get("mode", "hybrid")
    session_id = data.get("session_id", "default_session")

    if not question:
        return jsonify({"error": "Question parameter is required"}), 400

    result = RAGService.search_and_answer(db, question, mode, session_id)
    return jsonify(result), 200

@api_bp.route('/summarize', methods=['POST'])
def summarize():
    data = request.json or {}
    summary_type = data.get("type", "Executive")
    return jsonify(RAGService.summarize(db, summary_type)), 200

@api_bp.route('/compare', methods=['POST'])
def compare():
    return jsonify(RAGService.compare_documents(db)), 200

@api_bp.route('/classify', methods=['POST'])
def classify():
    if not db.documents:
        return jsonify({"error": "No uploaded document available to classify"}), 400
    latest_doc = list(db.documents.values())[-1]
    cat, conf = classifier.classify(latest_doc["text"], latest_doc["filename"])
    return jsonify({
        "filename": latest_doc["filename"],
        "predicted_category": cat,
        "confidence": conf
    }), 200

@api_bp.route('/analytics', methods=['GET'])
def analytics():
    total_chunks = sum(d["total_chunks"] for d in db.documents.values())
    return jsonify({
        "total_documents": len(db.documents),
        "total_processed_chunks": total_chunks,
        "total_embeddings_generated": total_chunks,
        "total_questions_answered": db.analytics["total_questions_answered"],
        "most_queried_documents": db.analytics["most_queried_documents"]
    }), 200
# 🤖 AI Research & Knowledge Assistant

A production-ready, full-stack web application that simplifies the process of exploring, understanding, and analyzing research papers. The application enables users to upload PDF documents, ask context-aware questions, generate summaries, compare multiple papers, and automatically classify research domains using a TensorFlow model.

The project follows a modular architecture based on the **Retrieval-Augmented Generation (RAG)** approach, ensuring that every response is generated from the uploaded documents and supported with page-level citations for better transparency and reliability.

# ✨ Features

### 📄 PDF Upload & Processing

* Upload one or more research papers in PDF format.
* Extracts clean text using **PyPDF**.
* Splits documents into overlapping chunks to preserve context and improve retrieval accuracy.

### 💬 Context-Aware Question Answering (RAG)

* Answers questions using only the information available in the uploaded documents.
* Provides page references and document names for easy verification.
* Minimizes irrelevant or unsupported responses by grounding answers in the source content.

### 🔍 Multiple Search Modes

Users can choose the most suitable retrieval strategy based on their requirements:

* **Hybrid Search** – Combines semantic similarity and keyword matching.
* **Semantic Search** – Retrieves content based on meaning and context.
* **Keyword Search** – Finds exact keyword matches within documents.

### 🧠 Research Paper Classification

* Uses a trained **TensorFlow/Keras** model to classify research papers into predefined categories such as:

  * Artificial Intelligence
  * Machine Learning
  * Natural Language Processing
  * Computer Vision
  * Cyber Security
  * Cloud Computing

### 📝 Smart Summarization

Generate summaries in different formats:

* Executive Summary
* Technical Summary
* Bullet Point Summary

### 📊 Document Comparison

Compare multiple research papers side by side to quickly identify similarities, differences, methodologies, and key findings.

### 📈 Analytics Dashboard

Monitor application activity through a live dashboard that displays:

* Total uploaded documents
* Number of processed chunks
* Generated embeddings
* User query statistics
* Overall system usage

---

# 🏗️ System Architecture

```text
                          Frontend Dashboard
                  (HTML5 • CSS3 • JavaScript)
                               │
                               │ REST APIs
                               ▼
                    Flask Backend API Layer
                         (routes/api.py)
      ┌────────────────────┬────────────────────┬───────────────────┐
      │                    │                    │
      ▼                    ▼                    ▼
Document Processor      RAG Engine      TensorFlow Classifier
    (PyPDF)           Search & QA         (.h5 Model)
      │                    │
      └──────────────┬─────┘
                     ▼
         In-Memory Knowledge Store
   (Documents • Chunks • Analytics • Context)
```

---

# 📂 Project Structure

```text
Research Assistant/
│
├── Backend/
│   ├── database/
│   │   └── db.py
│   │
│   ├── models/
│   │   ├── train_model.py
│   │   └── classifier.h5
│   │
│   ├── routes/
│   │   └── api.py
│   │
│   ├── services/
│   │   ├── document_processor.py
│   │   ├── rag_service.py
│   │   └── classifier_service.py
│   │
│   ├── uploads/
│   ├── .env.example
│   ├── app.py
│   └── requirements.txt
│
├── Frontend/
│   ├── index.html
│   ├── index.css
│   └── index.js
│
└── README.md
```

---

# 🛠️ Technology Stack

## Frontend

* HTML5
* CSS3
* JavaScript (ES6)
* Fetch API

## Backend

* Python 3
* Flask
* Flask-CORS

## Document Processing

* PyPDF

## Machine Learning

* TensorFlow (Keras)
* NumPy

## Environment Management

* python-dotenv

---

# 🚀 Getting Started

## Prerequisites

Before running the project, make sure you have:

* Python 3.9 or later
* pip (Python package manager)
* A modern web browser
* Visual Studio Code (recommended)

---

## 1. Install Dependencies

Navigate to the project directory and install the required packages.

```bash
pip install -r Backend/requirements.txt
```

---

## 2. Train the Classification Model

Generate the TensorFlow model used for document classification.

```bash
cd Backend/models
python train_model.py
cd ../..
```

This will create the following file:

```text
classifier.h5
```

---

## 3. Configure Environment Variables

Create a new environment configuration file.

```bash
cp Backend/.env.example Backend/.env
```

Update the environment variables if required.

---

## 4. Start the Flask Backend

```bash
cd Backend
python app.py
```

The backend server will start at:

```text
http://127.0.0.1:5000
```

---

## 5. Launch the Frontend

Open:

```text
Frontend/index.html
```

or launch the project using **VS Code Live Server**.

---

# 📡 REST API

| Endpoint              | Method | Description                          |
| --------------------- | ------ | ------------------------------------ |
| `/upload`             | POST   | Upload and process a PDF document    |
| `/documents`          | GET    | Retrieve all uploaded documents      |
| `/documents/<doc_id>` | DELETE | Delete a document                    |
| `/query`              | POST   | Perform RAG-based question answering |
| `/summarize`          | POST   | Generate document summaries          |
| `/compare`            | POST   | Compare multiple documents           |
| `/classify`           | POST   | Classify a research paper            |
| `/analytics`          | GET    | Retrieve dashboard analytics         |

---

# 💡 Design Decisions

### Context-Preserving Chunking

Documents are divided into **500-character chunks** with a **50-character overlap**. This overlap helps maintain sentence continuity and improves retrieval accuracy when information spans multiple chunks.

### Modular Architecture

The project is organized into independent layers for routing, services, models, and data storage. This separation makes the application easier to maintain, extend, and test.

### Retrieval-Augmented Generation (RAG)

Instead of generating answers from general knowledge, the system retrieves relevant document sections first and then generates responses based only on that retrieved context, improving reliability and reducing hallucinations.

### Graceful Error Handling

The classification service is designed to continue functioning even if TensorFlow dependencies are unavailable. This ensures that document upload, search, and summarization features remain operational.

### Lightweight Knowledge Store

An in-memory knowledge store is used to manage processed documents, text chunks, and application analytics. This keeps the project simple while allowing future integration with databases such as SQLite, PostgreSQL, or MongoDB.

---

# 🎯 Future Improvements

* Vector database integration (FAISS, ChromaDB, Pinecone)
* OCR support for scanned PDF documents
* User authentication and role-based access
* Conversation history with persistent memory
* Cloud deployment using Docker and Render
* Support for additional document formats such as DOCX and TXT
* Advanced filtering and search capabilities
* Interactive data visualizations for analytics

---

# 📌 Conclusion

The **AI Research & Knowledge Assistant** is designed to make reading and understanding technical documents faster and more efficient. By combining **Retrieval-Augmented Generation (RAG)** with **TensorFlow-based document classification**, the application delivers accurate, context-aware answers, meaningful summaries, intelligent document comparison, and automated research categorization within a clean and scalable architecture.

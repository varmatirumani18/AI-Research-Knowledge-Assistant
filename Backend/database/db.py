import uuid
from datetime import datetime

class KnowledgeBase:
    def __init__(self):
        self.documents = {}
        self.conversations = {}  # Session-based memory
        self.analytics = {
            "total_questions_answered": 0,
            "most_queried_documents": {}
        }

    def add_document(self, filename, text, num_pages, chunks):
        doc_id = str(uuid.uuid4())
        doc_meta = {
            "id": doc_id,
            "filename": filename,
            "upload_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_pages": num_pages,
            "total_chunks": len(chunks),
            "status": "PROCESSED",
            "text": text,
            "chunks": chunks
        }
        self.documents[doc_id] = doc_meta
        return doc_meta

    def list_documents(self):
        return [
            {
                "id": doc["id"],
                "filename": doc["filename"],
                "upload_timestamp": doc["upload_timestamp"],
                "total_pages": doc["total_pages"],
                "total_chunks": doc["total_chunks"],
                "status": doc["status"]
            }
            for doc in self.documents.values()
        ]

    def delete_document(self, doc_id):
        if doc_id in self.documents:
            del self.documents[doc_id]
            return True
        return False

    def update_analytics(self, doc_name=None):
        self.analytics["total_questions_answered"] += 1
        if doc_name:
            self.analytics["most_queried_documents"][doc_name] = \
                self.analytics["most_queried_documents"].get(doc_name, 0) + 1

    def save_chat_context(self, session_id, user_msg, assistant_msg):
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        self.conversations[session_id].append({
            "user": user_msg,
            "assistant": assistant_msg
        })

    def get_chat_context(self, session_id):
        return self.conversations.get(session_id, [])

db = KnowledgeBase()
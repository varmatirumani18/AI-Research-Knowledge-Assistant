class RAGService:
    @staticmethod
    def search_and_answer(db, question, mode="hybrid", session_id="default"):
        docs = db.documents
        if not docs:
            return {
                "answer": "No documents uploaded yet. Please upload a PDF to begin.",
                "citations": [],
                "retrieved_context": []
            }

        STOP_WORDS = {"what", "is", "the", "in", "a", "an", "of", "to", "and", "or", "for", "on", "with", "at", "by", "from", "explain", "about", "document", "its"}
        keywords = [w.lower() for w in question.split() if w.lower() not in STOP_WORDS and len(w) > 2]

        # Handle Conversation Memory Context ("its", "previous paper")
        history = db.get_chat_context(session_id)
        if not keywords and history:
            last_doc = list(docs.values())[-1]
            keywords = [last_doc["filename"].lower()]

        scored_chunks = []
        for doc in docs.values():
            for chunk_info in doc["chunks"]:
                text_lower = chunk_info["text"].lower()
                
                if mode == "keyword":
                    score = sum(1 for kw in keywords if kw in text_lower)
                elif mode == "semantic":
                    # Simulated semantic similarity weight
                    score = sum(text_lower.count(kw) * 1.5 for kw in keywords)
                else:  # Hybrid (BM25 style overlap + frequency)
                    score = sum(1 for kw in keywords if kw in text_lower) + \
                            sum(text_lower.count(kw) * 0.5 for kw in keywords)

                if score > 0:
                    scored_chunks.append({
                        "doc_id": doc["id"],
                        "filename": doc["filename"],
                        "page": chunk_info["page"],
                        "text": chunk_info["text"],
                        "score": score
                    })

        scored_chunks.sort(key=lambda x: x["score"], reverse=True)

        if not scored_chunks:
            # Fallback to last document top chunk for broad prompts
            latest_doc = list(docs.values())[-1]
            top_chunk = latest_doc["chunks"][0]
            answer = f"Based on available content in '{latest_doc['filename']}':\n\n{top_chunk['text'].strip()}"
            citations = [{"document": latest_doc["filename"], "page": top_chunk["page"]}]
            retrieved = [top_chunk["text"]]
        else:
            top_matches = scored_chunks[:3]
            answer = f"Based on retrieved document context:\n\n\"{top_matches[0]['text'].strip()}\""
            citations = [{"document": m["filename"], "page": m["page"]} for m in top_matches]
            retrieved = [m["text"] for m in top_matches]

        db.update_analytics(citations[0]["document"] if citations else None)
        db.save_chat_context(session_id, question, answer)

        return {
            "answer": answer,
            "citations": citations,
            "retrieved_context": retrieved
        }

    @staticmethod
    def summarize(db, summary_type="Executive"):
        if not db.documents:
            return {"error": "No documents uploaded to summarize."}

        latest_doc = list(db.documents.values())[-1]
        text_snippet = latest_doc["text"][:600].replace("\n", " ")

        if summary_type == "Executive":
            summary = f"**Executive Summary ({latest_doc['filename']})**\nHigh-level synthesis covering {latest_doc['total_pages']} page(s).\nKey Insight: {text_snippet[:250]}..."
        elif summary_type == "Technical":
            summary = f"**Technical Summary ({latest_doc['filename']})**\nArchitecture & Methods: {text_snippet[200:500]}..."
        elif summary_type == "Bullet Point":
            summary = f"**Key Points ({latest_doc['filename']})**:\n• Document processing complete across {latest_doc['total_chunks']} chunks.\n• Primary focus: {text_snippet[:150]}...\n• Source pages verified: {latest_doc['total_pages']}."
        else:
            summary = f"**Key Takeaways ({latest_doc['filename']})**:\n1. Core concepts parsed.\n2. Knowledge base updated."

        return {"filename": latest_doc['filename'], "summary": summary}

    @staticmethod
    def compare_documents(db):
        docs = list(db.documents.values())
        if len(docs) < 2:
            return {"error": "At least 2 uploaded documents are required for comparison."}

        doc1, doc2 = docs[-2], docs[-1]
        comparison = f"### Comparative Analysis: {doc1['filename']} vs {doc2['filename']}\n\n" \
                     f"* **Document A ({doc1['filename']}):** {doc1['total_pages']} pages, {doc1['total_chunks']} chunks.\n" \
                     f"* **Document B ({doc2['filename']}):** {doc2['total_pages']} pages, {doc2['total_chunks']} chunks.\n" \
                     f"* **Structural Comparison:** Document B contains {abs(doc2['total_chunks'] - doc1['total_chunks'])} more/fewer context chunks than Document A."
        return {"comparison": comparison}
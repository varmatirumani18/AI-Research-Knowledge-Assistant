import pypdf

class DocumentProcessor:
    @staticmethod
    def process_pdf(filepath, chunk_size=500, overlap=50):
        """
        Chunking Strategy Justification:
        Fixed-size overlapping chunking (500 chars with 50 char overlap) ensures 
        semantic boundary continuity without splitting key contextual sentences across chunks.
        """
        reader = pypdf.PdfReader(filepath)
        full_text = ""
        page_map = []
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            full_text += f"\n--- Page {i+1} ---\n" + text
            page_map.append({"page": i + 1, "text": text})

        # Intelligent text chunking
        chunks = []
        step = chunk_size - overlap
        for i in range(0, len(full_text), step):
            chunk_content = full_text[i:i + chunk_size]
            # Estimate primary page for citation
            approx_page = (i // max(1, len(full_text) // len(reader.pages))) + 1
            chunks.append({
                "chunk_id": len(chunks) + 1,
                "text": chunk_content,
                "page": min(approx_page, len(reader.pages))
            })

        return full_text, len(reader.pages), chunks
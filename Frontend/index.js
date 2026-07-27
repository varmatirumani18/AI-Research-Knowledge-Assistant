const API_BASE = "http://127.0.0.1:5000";
const uploadBtn = document.getElementById("uploadBtn");
const pdfInput = document.getElementById("pdf");
const status = document.getElementById("status");
const responseBox = document.getElementById("responseBox");
const documentList = document.getElementById("documentList");
const askBtn = document.getElementById("askBtn");
const questionInput = document.getElementById("question");

document.addEventListener("DOMContentLoaded", () => {
    refreshDocuments();
    refreshAnalytics();
    askBtn.addEventListener("click", handleAsk);
    uploadBtn.addEventListener("click", uploadPDF);
});

async function uploadPDF() {
    const file = pdfInput.files[0];
    if (!file) {
        status.style.color = "red";
        status.textContent = "Please select a PDF document.";
        return;
    }

    uploadBtn.disabled = true;
    uploadBtn.textContent = "Uploading...";
    status.style.color = "#2563eb";
    status.textContent = "Processing and indexing document...";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: formData });
        const data = await res.json();

        if (res.ok) {
            status.style.color = "green";
            status.textContent = data.message;
            pdfInput.value = "";
            refreshDocuments();
            refreshAnalytics();
            responseBox.innerHTML = `<b>Ingestion Complete:</b><br>Processed ${data.total_pages} page(s) into ${data.total_chunks} indexable chunks.`;
        } else {
            status.style.color = "red";
            status.textContent = data.error;
        }
    } catch (err) {
        status.style.color = "red";
        status.textContent = "Failed to connect to backend service.";
    }

    uploadBtn.disabled = false;
    uploadBtn.textContent = "Upload PDF";
}

async function handleAsk() {
    const question = questionInput.value.trim();
    const mode = document.getElementById("searchMode").value;

    if (!question) {
        responseBox.innerHTML = "<b style='color:red;'>Please enter a question first.</b>";
        return;
    }

    responseBox.innerHTML = "<i>Searching context and generating grounded answer...</i>";

    try {
        const res = await fetch(`${API_BASE}/query`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, mode, session_id: "user_session_1" })
        });
        const data = await res.json();

        let citationsHTML = "";
        if (data.citations && data.citations.length > 0) {
            citationsHTML = `<br><br><b>Citations & Sources:</b><br>` +
                data.citations.map(c => `• File: <i>${c.document}</i> (Page ${c.page})`).join("<br>");
        }

        responseBox.innerHTML = `${data.answer.replace(/\n/g, "<br>")}${citationsHTML}`;
        refreshAnalytics();
    } catch (err) {
        responseBox.innerHTML = "<b style='color:red;'>Failed to communicate with RAG endpoint.</b>";
    }
}

async function handleSummarize(type) {
    responseBox.innerHTML = `<i>Generating ${type} Summary...</i>`;
    try {
        const res = await fetch(`${API_BASE}/summarize`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ type })
        });
        const data = await res.json();
        responseBox.innerHTML = data.summary ? data.summary.replace(/\n/g, "<br>") : data.error;
    } catch (err) {
        responseBox.innerHTML = "<b style='color:red;'>Summarization failed.</b>";
    }
}

async function handleCompare() {
    responseBox.innerHTML = "<i>Comparing uploaded documents...</i>";
    try {
        const res = await fetch(`${API_BASE}/compare`, { method: "POST" });
        const data = await res.json();
        responseBox.innerHTML = data.comparison ? data.comparison.replace(/\n/g, "<br>") : data.error;
    } catch (err) {
        responseBox.innerHTML = "<b style='color:red;'>Comparison failed.</b>";
    }
}

async function handleClassify() {
    responseBox.innerHTML = "<i>Running TensorFlow classification inference...</i>";
    try {
        const res = await fetch(`${API_BASE}/classify`, { method: "POST" });
        const data = await res.json();
        if (data.error) {
            responseBox.innerHTML = `<b style='color:red;'>${data.error}</b>`;
        } else {
            responseBox.innerHTML = `<b>Document Classification Results:</b><br>` +
                `• File: <b>${data.filename}</b><br>` +
                `• Predicted Category: <b style='color:#2563eb;'>${data.predicted_category}</b><br>` +
                `• Model Confidence: <b>${data.confidence}</b>`;
        }
    } catch (err) {
        responseBox.innerHTML = "<b style='color:red;'>Classification failed.</b>";
    }
}

async function refreshDocuments() {
    try {
        const res = await fetch(`${API_BASE}/documents`);
        const data = await res.json();
        documentList.innerHTML = "";
        data.documents.forEach(doc => {
            const li = document.createElement("li");
            li.innerHTML = `
                <span><b>${doc.filename}</b> (${doc.total_pages} pages, ${doc.total_chunks} chunks)</span>
                <button class="delete" onclick="deleteDoc('${doc.id}')">Delete</button>
            `;
            documentList.appendChild(li);
        });
    } catch (err) {
        console.error("Error loading documents:", err);
    }
}

async function deleteDoc(docId) {
    try {
        await fetch(`${API_BASE}/documents/${docId}`, { method: "DELETE" });
        refreshDocuments();
        refreshAnalytics();
    } catch (err) {
        console.error("Delete failed:", err);
    }
}

async function refreshAnalytics() {
    try {
        const res = await fetch(`${API_BASE}/analytics`);
        const data = await res.json();
        document.getElementById("statDocs").textContent = data.total_documents;
        document.getElementById("statChunks").textContent = data.total_processed_chunks;
        document.getElementById("statQueries").textContent = data.total_questions_answered;
    } catch (err) {
        console.error("Error loading analytics:", err);
    }
}
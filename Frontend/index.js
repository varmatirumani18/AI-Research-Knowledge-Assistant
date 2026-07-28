const API_BASE = "https://ai-research-knowledge-assistant-xyl8.onrender.com";

document.addEventListener("DOMContentLoaded", () => {
    fetchAnalytics();
});

// Helper for UI Feedback
function showStatus(message, isError = false) {
    const statusEl = document.getElementById("statusMessage");
    if (statusEl) {
        statusEl.textContent = message;
        statusEl.className = isError ? "status-error" : "status-success";
    }
}

// Upload PDF Document
async function uploadDocument() {
    const fileInput = document.getElementById("pdfFile");
    if (!fileInput || !fileInput.files[0]) {
        alert("Please select a PDF file first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    showStatus("Uploading, processing, and indexing document...");

    try {
        const response = await fetch(`${API_BASE}/upload`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        if (response.ok) {
            showStatus(`Success: ${data.message || "Document uploaded successfully!"}`);
            fetchAnalytics();
        } else {
            showStatus(`Error: ${data.error || "Failed to upload document"}`, true);
        }
    } catch (err) {
        console.error("Upload error:", err);
        showStatus("Failed to connect to backend server.", true);
    }
}

// Ask Question (RAG Query)
async function askQuestion() {
    const queryInput = document.getElementById("userQuery");
    const modeSelect = document.getElementById("searchMode");
    const resultBox = document.getElementById("queryResult");

    if (!queryInput || !queryInput.value.trim()) {
        alert("Please enter a question.");
        return;
    }

    resultBox.textContent = "Searching document and generating answer...";

    try {
        const response = await fetch(`${API_BASE}/query`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                question: queryInput.value,
                mode: modeSelect ? modeSelect.value : "hybrid"
            })
        });

        const data = await response.json();
        if (response.ok) {
            resultBox.innerHTML = `<strong>Answer:</strong> ${data.answer}<br/><br/><em>Source Page: ${data.page || "N/A"}</em>`;
        } else {
            resultBox.textContent = `Error: ${data.error || "Query failed"}`;
        }
    } catch (err) {
        console.error("Query error:", err);
        resultBox.textContent = "Failed to connect to backend server.";
    }
}

// Get Executive Summary
async function getSummary() {
    const resultBox = document.getElementById("summaryResult");
    if (resultBox) resultBox.textContent = "Generating summary...";

    try {
        const response = await fetch(`${API_BASE}/summarize`, { method: "POST" });
        const data = await response.json();
        if (response.ok && resultBox) {
            resultBox.textContent = data.summary;
        } else if (resultBox) {
            resultBox.textContent = `Error: ${data.error || "Summarization failed"}`;
        }
    } catch (err) {
        console.error("Summary error:", err);
        if (resultBox) resultBox.textContent = "Failed to connect to backend server.";
    }
}

// Classify Document
async function classifyDocument() {
    const resultBox = document.getElementById("classifyResult");
    if (resultBox) resultBox.textContent = "Classifying document domain...";

    try {
        const response = await fetch(`${API_BASE}/classify`, { method: "POST" });
        const data = await response.json();
        if (response.ok && resultBox) {
            resultBox.textContent = `Predicted Domain: ${data.domain || data.category}`;
        } else if (resultBox) {
            resultBox.textContent = `Error: ${data.error || "Classification failed"}`;
        }
    } catch (err) {
        console.error("Classify error:", err);
        if (resultBox) resultBox.textContent = "Failed to connect to backend server.";
    }
}

// Fetch Analytics Stats
async function fetchAnalytics() {
    try {
        const response = await fetch(`${API_BASE}/analytics`);
        const data = await response.json();
        if (response.ok) {
            const statsEl = document.getElementById("analyticsStats");
            if (statsEl) {
                statsEl.textContent = `Documents: ${data.total_documents || 0} | Chunks: ${data.total_chunks || 0}`;
            }
        }
    } catch (err) {
        console.warn("Analytics fetch failed (server waking up):", err);
    }
}
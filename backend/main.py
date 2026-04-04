"""
main.py — FastAPI application
Endpoints:
  POST /upload          Upload + ingest a document
  POST /ask             Ask a question about a document
  POST /summarize       Summarize a document
  POST /flashcards      Generate flashcards from a document
  POST /exam-questions  Generate exam questions from a document
  GET  /documents       List all ingested documents
"""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
import shutil
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(title="مساعد الطالب الذكي", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOADS_DIR = Path(__file__).parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".pptx", ".docx"}


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class AskRequest(BaseModel):
    question: str
    doc_id: str | None = None
    top_k: int = 8


class SummarizeRequest(BaseModel):
    doc_id: str | None = None
    language: str = "ar"
    top_k: int = 20


class FlashcardsRequest(BaseModel):
    doc_id: str | None = None
    top_k: int = 20


class ExamRequest(BaseModel):
    doc_id: str | None = None
    top_k: int = 20


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    return {"message": "مساعد الطالب الذكي API — running"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF, PPTX, or DOCX file and ingest it into the vector store."""
    from extractor import extract
    from ingestor import ingest, is_already_ingested

    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{suffix}'. Allowed: {ALLOWED_EXTENSIONS}",
        )

    # Save to disk
    dest = UPLOADS_DIR / file.filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    # Deduplication check
    if is_already_ingested(dest):
        return {
            "status": "skipped",
            "message": "هذا الملف موجود بالفعل في قاعدة البيانات.",
            "filename": file.filename,
        }

    # Extract text
    extraction = extract(dest, filename=file.filename)
    if extraction.errors and not extraction.pages:
        raise HTTPException(status_code=422, detail=extraction.errors)

    # Ingest into ChromaDB
    summary = ingest(extraction, dest)

    return {
        "status": "ok",
        "filename": file.filename,
        "doc_id": summary["doc_id"],
        "chunks_added": summary["chunks_added"],
        "pages_skipped": summary["pages_skipped"],
        "warnings": summary["warnings"],
        "errors": summary["errors"],
    }


@app.post("/ask")
def ask_question(req: AskRequest) -> dict[str, Any]:
    """Answer a question using retrieved document chunks."""
    from retriever import retrieve
    from agent import answer_question

    chunks = retrieve(query=req.question, top_k=req.top_k, doc_id=req.doc_id)
    return answer_question(question=req.question, chunks=chunks)


@app.post("/summarize")
def summarize_document(req: SummarizeRequest) -> dict[str, Any]:
    """Summarize a document (or the whole collection if no doc_id given)."""
    from retriever import retrieve
    from agent import summarize

    # Use a broad query to pull representative chunks across the document
    chunks = retrieve(
        query="الأفكار الرئيسية والمفاهيم الأساسية",
        top_k=req.top_k,
        doc_id=req.doc_id,
    )
    summary_text = summarize(chunks=chunks, language=req.language)
    return {"summary": summary_text}


@app.post("/flashcards")
def create_flashcards(req: FlashcardsRequest) -> dict[str, Any]:
    """Generate flashcards from a document."""
    from retriever import retrieve
    from agent import generate_flashcards

    chunks = retrieve(
        query="المفاهيم والتعريفات والنقاط المهمة",
        top_k=req.top_k,
        doc_id=req.doc_id,
    )
    cards = generate_flashcards(chunks=chunks)
    return {"cards": cards, "count": len(cards)}


@app.post("/exam-questions")
def create_exam(req: ExamRequest) -> dict[str, Any]:
    """Generate MCQ and true/false exam questions from a document."""
    from retriever import retrieve
    from agent import generate_exam_questions

    chunks = retrieve(
        query="المفاهيم والحقائق الأساسية",
        top_k=req.top_k,
        doc_id=req.doc_id,
    )
    return generate_exam_questions(chunks=chunks)


@app.get("/documents")
def list_documents() -> dict[str, Any]:
    """List all unique documents currently stored in ChromaDB."""
    from ingestor import _get_collection

    collection = _get_collection()
    all_meta = collection.get(include=["metadatas"])["metadatas"]

    seen: dict[str, dict] = {}
    for m in all_meta:
        doc_id = m.get("doc_id", "")
        if doc_id not in seen:
            seen[doc_id] = {
                "doc_id": doc_id,
                "filename": m.get("filename", ""),
                "source_type": m.get("source_type", ""),
            }

    return {"documents": list(seen.values()), "total": len(seen)}


# ---------------------------------------------------------------------------
# Run directly: python main.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

"""
ingestor.py — chunk + embed + store in ChromaDB
Reads ExtractedPage objects from extractor.py and writes them to the vector store.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any

from extractor import ExtractionResult, ExtractedPage

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

CHROMA_PATH = Path(__file__).parent.parent / "chroma_db"
COLLECTION_NAME = "student_docs"
EMBED_MODEL = "intfloat/multilingual-e5-small"
CHUNK_SIZE = 512        # characters
CHUNK_OVERLAP = 64


# ---------------------------------------------------------------------------
# Lazy singletons (loaded once per process)
# ---------------------------------------------------------------------------

_embedder = None
_chroma_client = None
_collection = None


def _get_embedder():
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        logger.info("Loading embedding model '%s'...", EMBED_MODEL)
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder


def _get_collection():
    global _chroma_client, _collection
    if _collection is None:
        import chromadb
        _chroma_client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        _collection = _chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


# ---------------------------------------------------------------------------
# Chunker
# ---------------------------------------------------------------------------

def _chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Simple character-level sliding window chunker."""
    if not text.strip():
        return []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def _file_hash(filepath: str | Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def is_already_ingested(filepath: str | Path) -> bool:
    """Check if a file with the same SHA-256 hash is already in the vector store."""
    file_hash = _file_hash(filepath)
    collection = _get_collection()
    results = collection.get(where={"file_hash": file_hash}, limit=1)
    return len(results["ids"]) > 0


# ---------------------------------------------------------------------------
# Main ingest function
# ---------------------------------------------------------------------------

def ingest(result: ExtractionResult, filepath: str | Path) -> dict[str, Any]:
    """
    Chunk, embed, and store an ExtractionResult in ChromaDB.

    Returns a summary dict: {doc_id, chunks_added, pages_skipped, warnings}
    """
    file_hash = _file_hash(filepath)
    collection = _get_collection()
    embedder = _get_embedder()

    doc_id = file_hash[:16]   # short stable ID for this document
    chunks_added = 0
    pages_skipped = 0
    warnings: list[str] = []

    for page in result.pages:
        if page.warning:
            warnings.append(f"p{page.page_num}: {page.warning}")

        if not page.text.strip():
            pages_skipped += 1
            continue

        text_chunks = _chunk_text(page.text)
        if not text_chunks:
            pages_skipped += 1
            continue

        # Prefix required by multilingual-e5 for passage encoding
        prefixed = [f"passage: {c}" for c in text_chunks]
        embeddings = embedder.encode(prefixed, normalize_embeddings=True).tolist()

        ids = [
            f"{doc_id}_p{page.page_num}_c{i}"
            for i in range(len(text_chunks))
        ]
        metadatas = [
            {
                "filename": result.filename,
                "page_num": page.page_num,
                "source_type": page.source_type,
                "ocr_used": page.ocr_used,
                "chunk_index": i,
                "doc_id": doc_id,
                "file_hash": file_hash,
            }
            for i in range(len(text_chunks))
        ]

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=text_chunks,
            metadatas=metadatas,
        )
        chunks_added += len(text_chunks)

    logger.info(
        "Ingested '%s': %d chunks added, %d pages skipped",
        result.filename, chunks_added, pages_skipped,
    )

    return {
        "doc_id": doc_id,
        "filename": result.filename,
        "chunks_added": chunks_added,
        "pages_skipped": pages_skipped,
        "warnings": warnings,
        "errors": result.errors,
    }

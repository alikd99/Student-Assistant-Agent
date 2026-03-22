"""
retriever.py — query ChromaDB and return top-k relevant chunks
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class RetrievedChunk:
    text: str
    filename: str
    page_num: int
    source_type: str
    score: float          # cosine similarity (higher = more relevant)
    doc_id: str


def retrieve(
    query: str,
    top_k: int = 5,
    doc_id: str | None = None,        # filter to a single document
    filename: str | None = None,      # filter by original filename
) -> list[RetrievedChunk]:
    """
    Embed the query and return the top-k most relevant chunks from ChromaDB.

    Args:
        query:    The user's question or search text.
        top_k:    Number of chunks to return.
        doc_id:   If set, restrict search to this document only.
        filename: If set, restrict search to chunks from this filename.
    """
    from ingestor import _get_embedder, _get_collection

    embedder = _get_embedder()
    collection = _get_collection()

    # multilingual-e5 requires query prefix for query encoding
    query_embedding = embedder.encode(
        f"query: {query}", normalize_embeddings=True
    ).tolist()

    # Build optional metadata filter
    where: dict[str, Any] | None = None
    if doc_id and filename:
        where = {"$and": [{"doc_id": doc_id}, {"filename": filename}]}
    elif doc_id:
        where = {"doc_id": doc_id}
    elif filename:
        where = {"filename": filename}

    query_kwargs: dict[str, Any] = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
        "include": ["documents", "metadatas", "distances"],
    }
    if where:
        query_kwargs["where"] = where

    results = collection.query(**query_kwargs)

    chunks: list[RetrievedChunk] = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        # ChromaDB cosine distance: 0 = identical, 2 = opposite
        # Convert to similarity score in [0, 1]
        similarity = 1 - (dist / 2)
        chunks.append(
            RetrievedChunk(
                text=doc,
                filename=meta.get("filename", ""),
                page_num=meta.get("page_num", 0),
                source_type=meta.get("source_type", ""),
                score=round(similarity, 4),
                doc_id=meta.get("doc_id", ""),
            )
        )

    return chunks

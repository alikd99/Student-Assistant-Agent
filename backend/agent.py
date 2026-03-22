"""
agent.py — LLM calls: Q&A, summary, flashcards, exam questions
Supports: OpenAI API or LM Studio local server (OpenAI-compatible).
Set LLM_PROVIDER=lmstudio in .env to use LM Studio.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

from retriever import RetrievedChunk

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# OpenAI client (lazy)
# ---------------------------------------------------------------------------

_client = None


PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()  # "openai" or "lmstudio"

def _get_client():
    global _client
    if _client is None:
        from openai import OpenAI
        if PROVIDER == "lmstudio":
            _client = OpenAI(
                api_key=os.getenv("GROQ_API_KEY", "lm-studio"),
                base_url=os.getenv("LMSTUDIO_URL", "http://localhost:1234/v1"),
            )
        else:
            key = os.getenv("OPENAI_API_KEY")
            if not key:
                raise RuntimeError("OPENAI_API_KEY is not set in .env")
            _client = OpenAI(api_key=key)
    return _client


MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini" if PROVIDER == "openai" else "local-model")
MAX_TOKENS_QA = 1024
MAX_TOKENS_SUMMARY = 2048
MAX_TOKENS_FLASHCARDS = 2048
MAX_TOKENS_EXAM = 2048


def _chunks_to_context(chunks: list[RetrievedChunk]) -> str:
    parts = []
    for i, c in enumerate(chunks, start=1):
        parts.append(
            f"[Source {i} — {c.filename}, page {c.page_num}]\n{c.text}"
        )
    return "\n\n---\n\n".join(parts)


def _chat(system: str, user: str, max_tokens: int) -> str:
    client = _get_client()
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Q&A
# ---------------------------------------------------------------------------

def answer_question(question: str, chunks: list[RetrievedChunk]) -> dict[str, Any]:
    if not chunks:
        return {
            "answer": "لم أجد محتوى ذا صلة في الملفات المرفوعة. حاول إعادة صياغة السؤال.",
            "sources": [],
        }

    context = _chunks_to_context(chunks)
    system = (
        "You are an intelligent academic assistant. You have chunks from a study document and a student's question.\n"
        "Rules:\n"
        "1. If the answer is in the provided chunks, answer directly from them.\n"
        "2. If the question is about a well-known academic concept related to the document's topic, answer from your knowledge and mention it briefly.\n"
        "3. Only if the question is completely unrelated to the document or its topic, say so.\n"
        "4. Always reply in the same language the question was written in.\n"
        "5. Be helpful, clear, and detailed."
    )
    user = f"--- Document Chunks ---\n{context}\n\n--- Student Question ---\n{question}"

    answer_text = _chat(system, user, MAX_TOKENS_QA)
    sources = [
        {"filename": c.filename, "page_num": c.page_num, "score": c.score}
        for c in chunks
    ]
    return {"answer": answer_text, "sources": sources}


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def summarize(chunks: list[RetrievedChunk], language: str = "ar") -> str:
    if not chunks:
        return "لا يوجد محتوى للتلخيص."

    context = _chunks_to_context(chunks)
    lang_instruction = "in Arabic" if language == "ar" else "in English"
    system = f"Summarize the following study material {lang_instruction} using clear bullet points. Focus only on key concepts and important ideas."
    user = f"--- Content ---\n{context}"

    return _chat(system, user, MAX_TOKENS_SUMMARY)


# ---------------------------------------------------------------------------
# Flashcards
# ---------------------------------------------------------------------------

def generate_flashcards(chunks: list[RetrievedChunk]) -> list[dict[str, str]]:
    if not chunks:
        return []

    context = _chunks_to_context(chunks)
    system = (
        "You are an academic assistant. Output ONLY valid JSON with no extra text or markdown. "
        'Required format: {"cards": [{"q": "...", "a": "..."}]}'
    )
    user = (
        f"Based on the content below, generate 15 to 20 flashcards. "
        f"Use the same language as the content.\n\n--- Content ---\n{context}"
    )

    raw = _chat(system, user, MAX_TOKENS_FLASHCARDS).strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    try:
        return json.loads(raw).get("cards", [])
    except json.JSONDecodeError:
        logger.warning("Flashcard JSON parse failed. Raw:\n%s", raw)
        return []


# ---------------------------------------------------------------------------
# Exam questions
# ---------------------------------------------------------------------------

def generate_exam_questions(chunks: list[RetrievedChunk]) -> dict[str, Any]:
    if not chunks:
        return {"mcq": [], "true_false": []}

    context = _chunks_to_context(chunks)
    system = (
        "You are an academic assistant. Output ONLY valid JSON with no extra text or markdown. "
        'Required format: {"mcq": [{"question": "...", "options": ["A","B","C","D"], "correct_index": 0}], '
        '"true_false": [{"question": "...", "answer": true}]}'
    )
    user = (
        f"Based on the content below, generate 5 multiple choice questions and 5 true/false questions. "
        f"Use the same language as the content.\n\n--- Content ---\n{context}"
    )

    raw = _chat(system, user, MAX_TOKENS_EXAM).strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("Exam JSON parse failed. Raw:\n%s", raw)
        return {"mcq": [], "true_false": []}

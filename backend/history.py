"""
history.py — Persistent chat history using SQLite.
"""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "chat_history.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id     TEXT NOT NULL,
                role       TEXT NOT NULL,
                content    TEXT NOT NULL,
                sources    TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_doc_id ON messages(doc_id)")
        conn.commit()


def save_message(doc_id: str, role: str, content: str, sources=None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO messages (doc_id, role, content, sources) VALUES (?, ?, ?, ?)",
            (doc_id, role, content, json.dumps(sources) if sources else None),
        )
        conn.commit()


def load_history(doc_id: str) -> list[dict]:
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT role, content, sources, created_at FROM messages WHERE doc_id = ? ORDER BY id",
            (doc_id,),
        ).fetchall()
    result = []
    for row in rows:
        msg = {
            "role": row["role"],
            "content": row["content"],
            "created_at": row["created_at"],
        }
        if row["sources"]:
            msg["sources"] = json.loads(row["sources"])
        result.append(msg)
    return result


def clear_history(doc_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM messages WHERE doc_id = ?", (doc_id,))
        conn.commit()

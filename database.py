import sqlite3
from pathlib import Path

from src.config import SQLITE_DB_PATH


def get_connection():
    Path(SQLITE_DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                chapter TEXT NOT NULL,
                topic TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Not Started',
                deadline TEXT,
                priority TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def add_topic(subject, chapter, topic, deadline="", priority="Medium", notes=""):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO topics (subject, chapter, topic, deadline, priority, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (subject, chapter, topic, deadline, priority, notes),
        )


def list_topics():
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, subject, chapter, topic, status, deadline, priority, notes
            FROM topics
            ORDER BY subject, chapter, id
            """
        ).fetchall()
    return [dict(row) for row in rows]


def update_topic_status(topic_id, status):
    with get_connection() as conn:
        conn.execute("UPDATE topics SET status = ? WHERE id = ?", (status, topic_id))


def get_dashboard_stats():
    topics = list_topics()
    return {
        "total": len(topics),
        "completed": sum(1 for t in topics if t["status"] == "Completed"),
        "in_progress": sum(1 for t in topics if t["status"] == "In Progress"),
        "not_started": sum(1 for t in topics if t["status"] == "Not Started"),
    }
"""
database/db.py
---------------
SQLite connection helper + schema setup for the ZeNA AI Assistant.

Tables
------
users             -> leads collected from Explore Services & Business
                     Collaboration flows
chat_history      -> every message/response pair exchanged with the bot
session_requests  -> "Connect with Kirthika" booking requests
"""

import sqlite3
import os
from datetime import datetime

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "zena.db")


def get_connection():
    """Return a new SQLite connection with row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they do not already exist. Safe to call on
    every server startup."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            category TEXT,
            company_name TEXT,
            requirement TEXT,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            response TEXT,
            timestamp TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS session_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            purpose TEXT,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def log_chat(message: str, response: str):
    """Persist one turn of conversation."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO chat_history (message, response, timestamp) VALUES (?, ?, ?)",
        (message, response, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def get_chat_history(limit: int = 50):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM chat_history ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

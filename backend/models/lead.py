"""
models/lead.py
---------------
Data-access helpers for leads (users table) and Kirthika session
requests (session_requests table). Kept separate from db.py so the
connection/schema concerns stay isolated from "what a Lead looks like".
"""

from datetime import datetime
from database.db import get_connection


def create_lead(name, email, phone, category, requirement="", company_name=""):
    """Insert a new lead captured from Explore Services or Business
    Collaboration, and return its new row id."""
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO users (name, email, phone, category, company_name, requirement, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (name, email, phone, category, company_name, requirement, datetime.utcnow().isoformat()),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_leads():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def create_session_request(name, email, phone, purpose):
    """Insert a new 'Connect with Kirthika' booking request."""
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO session_requests (name, email, phone, purpose, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, email, phone, purpose, datetime.utcnow().isoformat()),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_all_session_requests():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM session_requests ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(row) for row in rows]

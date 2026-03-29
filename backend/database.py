import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "./pariksha_audit.db"

def init_db():
    """Create database and tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS verifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        article_preview TEXT,
        article_length INTEGER,
        claims_found INTEGER,
        credibility_score INTEGER,
        credibility_label TEXT,
        verified_count INTEGER,
        contradicted_count INTEGER,
        unverified_count INTEGER,
        source_quality TEXT,
        bias_score INTEGER,
        bias_type TEXT,
        full_result TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized.")


def log_verification(article_text: str, result: dict):
    """Save a verification result to the audit log."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO verifications (
        timestamp, article_preview, article_length,
        claims_found, credibility_score, credibility_label,
        verified_count, contradicted_count, unverified_count,
        source_quality, bias_score, bias_type, full_result
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        article_text[:200],
        result.get("article_length", 0),
        result.get("claims_found", 0),
        result.get("credibility_score", 0),
        result.get("credibility_label", "UNKNOWN"),
        result.get("verified_count", 0),
        result.get("contradicted_count", 0),
        result.get("unverified_count", 0),
        result.get("source_report", {}).get("overall_source_quality", "N/A"),
        result.get("bias_report", {}).get("bias_score", 0),
        result.get("bias_report", {}).get("bias_type", "N/A"),
        json.dumps(result)
    ))

    conn.commit()
    conn.close()


def get_all_verifications():
    """Retrieve all past verifications for the dashboard."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, timestamp, article_preview, credibility_score,
           credibility_label, claims_found, verified_count,
           contradicted_count, bias_type
    FROM verifications
    ORDER BY timestamp DESC
    LIMIT 50
    """)

    rows = cursor.fetchall()
    conn.close()

    columns = [
        "id", "timestamp", "article_preview", "credibility_score",
        "credibility_label", "claims_found", "verified_count",
        "contradicted_count", "bias_type"
    ]

    return [dict(zip(columns, row)) for row in rows]
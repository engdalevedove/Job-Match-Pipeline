import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/jobs_history.db")


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS seen_jobs (
                job_hash TEXT PRIMARY KEY,
                title TEXT,
                company TEXT,
                site TEXT,
                job_url TEXT,
                score INTEGER,
                created_at TEXT
            )
        """)
        conn.commit()


def generate_job_hash(title: str, company: str, job_url: str) -> str:
    raw_key = f"{str(title).strip().lower()}|{str(company).strip().lower()}"
    if not company or str(company).lower() == "nan":
        raw_key = str(job_url).strip()
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def is_job_seen(job_hash: str) -> bool:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT 1 FROM seen_jobs WHERE job_hash = ?", (job_hash,))
        return cursor.fetchone() is not None


def save_job(job_hash: str, title: str, company: str, site: str, job_url: str, score: int) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR IGNORE INTO seen_jobs (job_hash, title, company, site, job_url, score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (job_hash, title, company, site, job_url, score, datetime.utcnow().isoformat()))
        conn.commit()
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "test.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active'
);
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """テーブルがなければ作る"""
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def execute(sql: str, params: tuple = ()):
    """INSERT / UPDATE / DELETE を実行する"""
    conn = get_connection()
    try:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def fetch_all(sql: str, params: tuple = ()) -> list[dict]:
    """SELECT の結果を、全行まとめて返す"""
    conn = get_connection()
    try:
        return [dict(row) for row in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()


def fetch_one(sql: str, params: tuple = ()) -> dict | None:
    """SELECT の結果の、1行目だけを返す(なければ None)"""
    rows = fetch_all(sql, params)
    return rows[0] if rows else None

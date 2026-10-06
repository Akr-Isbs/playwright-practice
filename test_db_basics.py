import sqlite3

import pytest


def test_users_table_is_empty_at_start(db):
    count = db.fetch_one("SELECT COUNT(*) AS cnt FROM users")["cnt"]
    assert count == 0


def test_insert_and_select_user(db):
    db.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        ("taro", "taro@example.com"),
    )
    user = db.fetch_one(
        "SELECT username, email, status FROM users WHERE username = ?",
        ("taro",),
    )
    assert user == {"username": "taro", "email": "taro@example.com", "status": "active"}


def test_update_user_status(db):
    db.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        ("taro", "taro@example.com"),
    )
    db.execute("UPDATE users SET status = ? WHERE username = ?", ("locked", "taro"))
    user = db.fetch_one("SELECT status FROM users WHERE username = ?", ("taro",))
    assert user["status"] == "locked"


def test_duplicate_username_is_rejected(db):
    db.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        ("taro", "taro@example.com"),
    )
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            ("taro", "other@example.com"),
        )

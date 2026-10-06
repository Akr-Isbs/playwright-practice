import pytest
from playwright.sync_api import expect


def test_register_user_is_saved_in_db(register_page, db):
    """画面から登録すると、DBに保存される"""
    register_page.open()
    register_page.register("taro", "taro@example.com")

    expect(register_page.message).to_have_text("登録しました")
    user = db.fetch_one(
        "SELECT username, email, status FROM users WHERE username = ?",
        ("taro",),
    )
    assert user == {"username": "taro", "email": "taro@example.com", "status": "active"}


def test_seeded_users_are_listed(user_list_page, db):
    """DBに入れておいたデータが、一覧に表示される"""
    db.execute(
        "INSERT INTO users (username, email, status) VALUES (?, ?, ?)",
        ("hanako", "hanako@example.com", "active"),
    )
    db.execute(
        "INSERT INTO users (username, email, status) VALUES (?, ?, ?)",
        ("jiro", "jiro@example.com", "locked"),
    )

    user_list_page.open()

    expect(user_list_page.rows).to_have_count(2)
    expect(user_list_page.row_for("hanako")).to_contain_text("hanako@example.com")
    expect(user_list_page.row_for("jiro")).to_contain_text("locked")


def test_duplicate_username_shows_error_and_does_not_add_row(register_page, db):
    """同じユーザー名で登録すると、エラーになり、DBの件数は増えない"""
    db.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        ("taro", "taro@example.com"),
    )

    register_page.open()
    register_page.register("taro", "other@example.com")

    expect(register_page.message).to_have_text("このユーザー名は既に使われています")
    count = db.fetch_one("SELECT COUNT(*) AS cnt FROM users")["cnt"]
    assert count == 1


@pytest.mark.parametrize(
    "username, email",
    [
        ("", "taro@example.com"),
        ("taro", ""),
        ("", ""),
    ],
    ids=["empty_username", "empty_email", "both_empty"],
)
def test_required_fields_show_error_and_do_not_save(register_page, db, username, email):
    """必須項目が空だと、エラーになり、DBには保存されない"""
    register_page.open()
    register_page.register(username, email)

    expect(register_page.message).to_have_text("ユーザー名とメールアドレスは必須です")
    count = db.fetch_one("SELECT COUNT(*) AS cnt FROM users")["cnt"]
    assert count == 0

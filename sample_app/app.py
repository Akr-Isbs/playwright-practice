import sqlite3

from flask import Flask, render_template_string, request

from db import database

app = Flask(__name__)

LIST_PAGE = """
<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>ユーザー一覧</title></head>
<body>
  <h1>ユーザー一覧</h1>
  <a href="/register">新規登録</a>
  <table border="1">
    <thead><tr><th>ユーザー名</th><th>メールアドレス</th><th>状態</th></tr></thead>
    <tbody>
      {% for u in users %}
      <tr><td>{{ u.username }}</td><td>{{ u.email }}</td><td>{{ u.status }}</td></tr>
      {% endfor %}
    </tbody>
  </table>
</body>
</html>
"""

REGISTER_PAGE = """
<!doctype html>
<html lang="ja">
<head><meta charset="utf-8"><title>ユーザー登録</title></head>
<body>
  <h1>ユーザー登録</h1>
  {% if message %}<p role="alert">{{ message }}</p>{% endif %}
  <form method="post">
    <label for="username">ユーザー名</label>
    <input id="username" name="username" value="{{ username }}"><br>
    <label for="email">メールアドレス</label>
    <input id="email" name="email" value="{{ email }}"><br>
    <button type="submit">登録</button>
  </form>
  <a href="/">一覧へ</a>
</body>
</html>
"""


@app.route("/")
def index():
    users = database.fetch_all("SELECT username, email, status FROM users ORDER BY id")
    return render_template_string(LIST_PAGE, users=users)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template_string(REGISTER_PAGE, message="", username="", email="")

    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()

    if not username or not email:
        message = "ユーザー名とメールアドレスは必須です"
        return render_template_string(REGISTER_PAGE, message=message, username=username, email=email)

    try:
        database.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
    except sqlite3.IntegrityError:
        message = "このユーザー名は既に使われています"
        return render_template_string(REGISTER_PAGE, message=message, username=username, email=email)

    return render_template_string(REGISTER_PAGE, message="登録しました", username="", email="")


if __name__ == "__main__":
    database.init_db()
    app.run(host="127.0.0.1", port=5055)

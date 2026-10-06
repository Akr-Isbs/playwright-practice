import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import Page

from db import database
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.user_list_page import UserListPage

PROJECT_ROOT = Path(__file__).resolve().parent
APP_URL = "http://127.0.0.1:5055"


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    """ログイン済みの状態で、商品一覧画面の担当者を渡す"""
    login = LoginPage(page)
    login.open()
    login.login("standard_user", "secret_sauce")
    return InventoryPage(page)


@pytest.fixture
def db():
    """テストごとに、空のusersテーブルを用意し、終わったら片付ける"""
    database.init_db()
    database.execute("DELETE FROM users")
    yield database
    database.execute("DELETE FROM users")


@pytest.fixture(scope="session")
def app_server():
    """練習用アプリを起動し、全テストが終わったら止める"""
    database.init_db()
    proc = subprocess.Popen(
        [sys.executable, "-m", "sample_app.app"],
        cwd=PROJECT_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(50):
        try:
            urllib.request.urlopen(APP_URL, timeout=1)
            break
        except Exception:
            time.sleep(0.2)
    else:
        proc.terminate()
        raise RuntimeError("練習用アプリが起動しませんでした")
    yield APP_URL
    proc.terminate()
    proc.wait()


@pytest.fixture
def register_page(page: Page, app_server: str, db) -> RegisterPage:
    return RegisterPage(page, app_server)


@pytest.fixture
def user_list_page(page: Page, app_server: str, db) -> UserListPage:
    return UserListPage(page, app_server)

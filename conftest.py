import pytest
from playwright.sync_api import Page

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


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


from db import database


@pytest.fixture
def db():
    """テストごとに、空のusersテーブルを用意し、終わったら片付ける"""
    database.init_db()
    database.execute("DELETE FROM users")
    yield database
    database.execute("DELETE FROM users")

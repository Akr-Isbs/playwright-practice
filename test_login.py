from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_login_success(page: Page, login_page: LoginPage):
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


def test_login_failure(login_page: LoginPage):
    login_page.open()
    login_page.login("standard_user", "wrong_password")
    expect(login_page.login_error).to_be_visible()


def test_add_to_cart(inventory_page: InventoryPage):
    inventory_page.add_first_item_to_cart()
    expect(inventory_page.cart_badge).to_have_text("1")


def test_add_two_items_to_cart(inventory_page: InventoryPage):
    inventory_page.add_first_item_to_cart()
    inventory_page.add_first_item_to_cart()
    expect(inventory_page.cart_badge).to_have_text("2")


def test_remove_item_from_cart(inventory_page: InventoryPage):
    inventory_page.add_first_item_to_cart()
    inventory_page.remove_first_item_from_cart()
    expect(inventory_page.cart_badge).to_have_count(0)

import pytest
from playwright.sync_api import Page


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    return page

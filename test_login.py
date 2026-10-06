from playwright.sync_api import Page, expect


def test_login_success(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


def test_login_failure(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("wrong_password")
    page.get_by_role("button", name="Login").click()
    expect(page.get_by_text("Username and password do not match")).to_be_visible()


def test_add_to_cart(logged_in_page: Page):
    logged_in_page.get_by_role("button", name="Add to cart").first.click()
    expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text("1")


def test_add_two_items_to_cart(logged_in_page: Page):
    logged_in_page.get_by_role("button", name="Add to cart").first.click()
    logged_in_page.get_by_role("button", name="Add to cart").first.click()
    expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text("2")

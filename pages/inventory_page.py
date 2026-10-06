from playwright.sync_api import Page


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.add_to_cart_buttons = page.get_by_role("button", name="Add to cart")
        self.remove_buttons = page.get_by_role("button", name="Remove")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def add_first_item_to_cart(self):
        self.add_to_cart_buttons.first.click()

    def remove_first_item_from_cart(self):
        self.remove_buttons.first.click()

from playwright.sync_api import Locator, Page


class UserListPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.rows = page.locator("tbody tr")

    def open(self):
        self.page.goto(f"{self.base_url}/")

    def row_for(self, username: str) -> Locator:
        """指定したユーザー名を含む行を返す"""
        return self.rows.filter(has_text=username)

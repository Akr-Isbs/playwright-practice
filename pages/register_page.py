from playwright.sync_api import Page


class RegisterPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.username_input = page.get_by_label("ユーザー名")
        self.email_input = page.get_by_label("メールアドレス")
        self.submit_button = page.get_by_role("button", name="登録")
        self.message = page.get_by_role("alert")

    def open(self):
        self.page.goto(f"{self.base_url}/register")

    def register(self, username: str, email: str):
        self.username_input.fill(username)
        self.email_input.fill(email)
        self.submit_button.click()

from .base_page import BasePage


class LoginPage(BasePage):
    """Page object for the login page."""

    def goto(self, base_url: str, broken: bool = False):
        """Navigate to the login page or its broken variant."""
        path = "/login" if not broken else "/login?broken=1"
        url = base_url.rstrip("/") + path
        self.driver.get(url)

    def fill_username(self, value: str):
        self.H("login.usernameInput").send_keys(value)

    def fill_password(self, value: str):
        self.H("login.passwordInput").send_keys(value)

    def submit(self):
        self.H("login.submit").click()
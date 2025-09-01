from .base_page import BasePage

class LoginPage(BasePage):
    def goto(self, base_url: str, broken: bool = False):
        path = "/login?variant=broken" if broken else "/login"
        self.driver.get(base_url + path)

    def fill_username(self, value: str, broken: bool = False):
        locator = "login.usernmeInput" if broken else "login.usernameInput"
        self.H(locator).send_keys(value)

    def fill_password(self, value: str, broken: bool = False):
        locator = "login.passwrdInput" if broken else "login.passwordInput"
        self.H(locator).send_keys(value)

    def submit(self):
        self.H("login.submit").click()

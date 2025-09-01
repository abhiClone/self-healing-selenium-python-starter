from selenium.webdriver.remote.webdriver import WebDriver
from src.heal.healer import Healer


class BasePage:
    """Base page object that wraps Selenium driver with a healer."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.healer = Healer(driver)

    def H(self, element_id: str):
        """Use the healer to find an element by logical ID."""
        return self.healer.find(element_id)
from selenium.webdriver.remote.webdriver import WebDriver
from src.heal.healer import Healer

class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.healer = Healer(driver)

    def H(self, element_id: str):
        return self.healer.find(element_id)

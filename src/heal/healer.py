from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from .registry import LocatorRegistry
from .types import Strategy


class Healer:
    """
    A simple self-healing helper for Selenium WebDriver.
    It tries the first locator strategy; if it fails, it tries fallbacks
    and proposes an update to the registry when a fallback succeeds.
    """

    def __init__(self, driver: WebDriver, registry: Optional[LocatorRegistry] = None) -> None:
        self.driver = driver
        self.registry = registry or LocatorRegistry()

    def find(self, element_id: str) -> WebElement:
        entry = self.registry.get(element_id)
        strategies = entry.strategies
        for idx, strat in enumerate(strategies):
            try:
                element = self._find_by_strategy(strat)
                # If this is a fallback (not first), propose an update
                if idx != 0:
                    self.registry.propose_update(element_id, strat)
                return element
            except Exception:
                # Ignore and try next strategy
                continue
        raise ValueError(f"Unable to locate element '{element_id}' via strategies {strategies}")

    def _find_by_strategy(self, strat: Strategy) -> WebElement:
        by_map = {
            'id': By.ID,
            'css': By.CSS_SELECTOR,
            'xpath': By.XPATH,
            'name': By.NAME
        }
        by = by_map.get(strat.type)
        if by is None:
            raise ValueError(f"Unknown strategy type '{strat.type}'")
        elements = self.driver.find_elements(by, strat.value)
        if len(elements) == 1:
            return elements[0]
        elif len(elements) == 0:
            raise Exception("No elements found")
        else:
            raise Exception("Multiple elements found")
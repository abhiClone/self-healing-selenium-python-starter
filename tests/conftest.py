import threading
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scripts.demo_server import run_app


@pytest.fixture(scope="session")
def base_url():
    """Start the demo Flask server in a background thread for the test session."""
    port = 5001
    thread = threading.Thread(target=run_app, kwargs={'port': port}, daemon=True)
    thread.start()
    # Wait for server to be ready
    time.sleep(1)
    yield f"http://localhost:{port}"
    # Server runs as daemon; will exit on teardown


@pytest.fixture
def driver():
    """Create a headless Chrome WebDriver for each test."""
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
import os, threading, time, pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scripts.demo_server import create_app

@pytest.fixture(scope="session", autouse=True)
def demo_server():
    app = create_app()
    port = 3000
    th = threading.Thread(target=lambda: app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False), daemon=True)
    th.start()
    time.sleep(0.8)
    yield

@pytest.fixture(scope="session")
def base_url():
    return "http://127.0.0.1:3000"

@pytest.fixture
def driver():
    opts = Options()
    headless = os.environ.get("HEADLESS", "1") != "0"
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,800")
    driver = webdriver.Chrome(options=opts)  # Selenium Manager resolves chromedriver
    yield driver
    driver.quit()

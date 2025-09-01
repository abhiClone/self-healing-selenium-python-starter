from src.pages.login_page import LoginPage

def test_login_valid(driver, base_url):
    page = LoginPage(driver)
    page.goto(base_url, broken=False)
    page.fill_username("demo", broken=False)
    page.fill_password("pass", broken=False)
    page.submit()
    assert "/dashboard" in driver.current_url

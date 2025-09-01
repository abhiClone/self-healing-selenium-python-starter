from src.pages.login_page import LoginPage

def test_login_normal(driver, base_url):
    page = LoginPage(driver)
    page.goto(base_url, broken=False)
    page.fill_username("demo")
    page.fill_password("pass")
    page.submit()
    assert "/dashboard" in driver.current_url

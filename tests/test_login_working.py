from src.pages.login_page import LoginPage


def test_login_valid(driver, base_url):
    """Ensure login works when using the correct locators."""
    page = LoginPage(driver)
    page.goto(base_url, broken=False)
    page.fill_username("demo")
    page.fill_password("pass")
    page.submit()
    # After form submit, should navigate to dashboard page
    assert "dashboard" in driver.current_url
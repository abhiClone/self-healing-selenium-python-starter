from src.pages.login_page import LoginPage


def test_login_valid(driver, base_url):
    """Ensure login still works when primary locators break and healing fallback is used."""
    page = LoginPage(driver)
    # Load broken variant of login page
    page.goto(base_url, broken=True)
    page.fill_username("demo")
    page.fill_password("pass")
    page.submit()
    # Should still navigate to dashboard due to self-healing fallback
    assert "dashboard" in driver.current_url
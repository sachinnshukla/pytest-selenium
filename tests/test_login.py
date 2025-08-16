# Example test file: test_login.py
import pytest
from pages.saucelab_login_page import SauceLabLoginPage
from pages.saucelabs_home_page import SauceLabHomePage 

class TestLogin:
    def test_login_valid_user(self, driver, test_environment):
        login_page = SauceLabLoginPage(driver)
        login_page.enter_username(test_environment.username)
        login_page.enter_password(test_environment.password)
        login_page.click_login()
        home_page = SauceLabHomePage(driver)
        assert home_page.is_home_page_displayed(), "User should be logged in successfully"

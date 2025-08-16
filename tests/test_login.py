# Simple test file: test_login.py
import pytest
from pages.saucelab_login_page import SauceLabLoginPage
from pages.saucelabs_home_page import SauceLabHomePage
from config import config

class TestLogin:
    def test_login_valid_user(self, driver):
        login_page = SauceLabLoginPage(driver)
        login_page.enter_username(config.USERNAME)
        login_page.enter_password(config.PASSWORD)
        login_page.click_login()
        home_page = SauceLabHomePage(driver)
        assert home_page.is_home_page_displayed(), "User should be logged in successfully"

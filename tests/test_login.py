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
    
    def test_login_invalid_user_fail_demo(self, driver, take_screenshot):
        """Test designed to fail and capture screenshot"""
        login_page = SauceLabLoginPage(driver)
        
        # Use invalid credentials to make test fail
        login_page.enter_username("invalid_user")
        login_page.enter_password("wrong_password")
        login_page.click_login()
        
        # Take a manual screenshot before the assertion fails
        take_screenshot("before_assertion_failure")
        
        # This assertion will fail, triggering automatic screenshot
        home_page = SauceLabHomePage(driver)
        assert home_page.is_home_page_displayed(), "❌ This test is designed to FAIL for screenshot testing"
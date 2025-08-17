from pages.saucelab_login_page import SauceLabLoginPage
from pages.saucelabs_home_page import SauceLabHomePage
from config import config

class TestLogin:
    def test_login_valid_user(self, driver):
        """Test successful login with valid credentials"""
        login_page = SauceLabLoginPage(driver)
        login_page.enter_username(config.USERNAME)
        login_page.enter_password(config.PASSWORD)
        login_page.click_login()
        home_page = SauceLabHomePage(driver)
        assert home_page.is_home_page_displayed(), "User should be logged in successfully"
    
    def test_pipeline_robustness_demo(self, driver, take_screenshot):
        login_page = SauceLabLoginPage(driver)
        
        # Use invalid credentials that will fail
        login_page.enter_username("invalid_user")
        login_page.enter_password("wrong_password")
        login_page.click_login()
        
        # Take screenshot before the expected failure
        take_screenshot("demo_invalid_login_attempt")
        
        # This will fail, but pipeline should continue! 
        home_page = SauceLabHomePage(driver)
        assert home_page.is_home_page_displayed(), "❌ DEMO: Pipeline should handle this failure gracefully and still deploy dashboard"
    

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage  # Use relative import

class SauceLabLoginPage(BasePage):
    USERNAME_FIELD = (By.XPATH, "//input[@placeholder = 'Username']")
    PASSWORD_FIELD = (By.XPATH, "//input[@placeholder = 'Password']")
    LOGIN_BUTTON = (By.XPATH, "//input[@id= 'login-button']")

    def enter_username(self, username):
        username_elem = self.wait.until(EC.visibility_of_element_located(self.USERNAME_FIELD))
        username_elem.clear()
        username_elem.send_keys(username)

    def enter_password(self, password):
        password_elem = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        password_elem.clear()
        password_elem.send_keys(password)

    def click_login(self):
        login_btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_btn.click()
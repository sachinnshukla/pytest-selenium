from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class SauceLabHomePage(BasePage):
    HOMEPAGE_IDENTIFIER = (By.XPATH, "//span[@class='title' and contains(text(),'Products')]")

    def is_home_page_displayed(self):
        home_page_elem = self.wait.until(EC.visibility_of_element_located(self.HOMEPAGE_IDENTIFIER))
        return home_page_elem.is_displayed()
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME))
        return self

    def login(self, username, password):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME)).send_keys(username)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        self.wait.until(EC.visibility_of_element_located(self.INVENTORY_CONTAINER))
        return self

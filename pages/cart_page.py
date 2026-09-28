from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CartPage:
    CART_LIST = (By.CSS_SELECTOR, ".cart_list")
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_until_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.CART_LIST))
        return self

    def product_names(self):
        return [element.text for element in self.driver.find_elements(*self.ITEM_NAMES)]

    def product_prices(self):
        return [element.text for element in self.driver.find_elements(*self.ITEM_PRICES)]

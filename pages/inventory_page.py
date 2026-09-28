from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class InventoryPage:
    INVENTORY_LIST = (By.CSS_SELECTOR, ".inventory_list")
    INVENTORY_ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    ITEM_NAMES = (By.CSS_SELECTOR, ".inventory_item_name")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_until_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.INVENTORY_LIST))
        return self

    def product_names(self):
        return [element.text for element in self.driver.find_elements(*self.ITEM_NAMES)]

    def product_prices(self):
        return [element.text for element in self.driver.find_elements(*self.ITEM_PRICES)]

    def add_product(self, product_name):
        item = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//div[contains(@class,'inventory_item')][.//div[contains(@class,'inventory_item_name') and normalize-space()=\"{product_name}\"]]")))
        item.find_element(By.CSS_SELECTOR, "button").click()
        return self

    def cart(self):
        self.driver.find_element(*self.CART_LINK).click()

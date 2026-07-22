# pages/cart_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage

class CartPage(BasePage):
    # JPetStore 购物车页元素定位器
    CHECKOUT_BUTTON = (By.LINK_TEXT, "Proceed to Checkout")
    CHECKOUT_TITLE = (By.XPATH, "//h2[text()='Shopping Cart']")
    def is_cart_page_loaded(self):
        """验证购物车页面是否加载成功"""
        return "Shopping Cart" in self.get_text(self.CHECKOUT_TITLE)

    def go_to_checkout(self):
        """进入结算页面"""
        self.click(self.CHECKOUT_BUTTON)
        return CheckoutPage(self.driver)
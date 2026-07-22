# pages/product_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.cart_page import CartPage

class ProductPage(BasePage):
    # JPetStore 商品详情页元素定位器
    ADD_TO_CART_BUTTON = (By.LINK_TEXT, "Add to Cart")

    def add_to_cart(self):
        """将商品加入购物车"""
        self.click(self.ADD_TO_CART_BUTTON)
        return CartPage(self.driver) # 返回购物车页对象
#pages/product_page.py
from pages.base_page import BasePage
from pages.cart_page import CartPage

class ProductPage(BasePage):
    ADD_TO_CART_BUTTON = "a:has-text('Add to Cart')"
    PRODUCT_TITLE = "h2:has-text('Product ID')"

    def add_to_cart(self) -> CartPage:
        """点击加入购物车， 返回 CartPage"""
        self.click(self.ADD_TO_CART_BUTTON)
        return CartPage(self.page)


    def get_product_title(self) -> str:
        """获取商品标题，用于断言"""
        return self.get_text(self.PRODUCT_TITLE)


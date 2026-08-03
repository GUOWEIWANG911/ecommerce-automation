#pages/cart_page.py
from pages.base_page import BasePage

class CartPage(BasePage):
    CART_HEADER = "h2:has-text('Shopping Cart')"
    CHECKOUT_BUTTON = "a:has-text('Proceed to Checkout')"
    ITEM_COUNT = "table tr:nth-child(2) td:nth-child(1)"

    def is_cart_visible(self) -> bool:
        """检查购物车页面是否加载"""
        return self.is_visible(self.CART_HEADER)


    def proceed_to_checkout(self) -> "CheckoutPage":
        from pages.checkout_page import CheckoutPage
        self.click(self.CHECKOUT_BUTTON)
        return CheckoutPage(self.page)


    def get_item_count(self) -> int:
        """获取购物车商品数量"""
        text = self.get_text(self.ITEM_COUNT)
        return int(text) if text.isdigit() else 0



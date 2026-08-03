# pages/confirmation_page.py
from pages.base_page import BasePage

class ConfirmationPage(BasePage):
    """订单确认页面，用于验证订单提交成功并获取订单号"""

    # 修正4: 使用语义化定位器，避免 XPath 硬编码
    SUCCESS_MESSAGE = "li:has-text('Thank you, your order has been submitted')"
    ORDER_ID_HEADER = "th:has-text('Order #')"
    RETURN_HOME_LINK = "a:has-text('Return to Main Menu')"

    def is_order_submitted(self) -> bool:
        """验证订单是否提交成功"""
        return self.is_visible(self.SUCCESS_MESSAGE)


    def get_order_id(self) -> str | None:
        """提取订单号"""
        text = self.get_text(self.ORDER_ID_HEADER)
        if not text:
            return None
        # 清洗逻辑：提取 "Order #25158" 部分
        parts = text.split()
        if len(parts) >= 2:
            return f"{parts[0]} {parts[1]}"
        return text


    def go_to_home(self) -> "HomePage":
        """点击返回主页"""
        from pages.home_page import HomePage
        self.click(self.RETURN_HOME_LINK)
        return HomePage(self.page)


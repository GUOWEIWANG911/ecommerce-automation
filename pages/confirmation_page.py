from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ConfirmationPage(BasePage):
    """
    订单确认页面 (Order Confirmation)
    用于验证订单是否提交成功并获取订单号
    """

    # --- 元素定位器 (Locators) ---
    
    # 1. 成功提示文本: "Thank you, your order has been submitted."
    SUCCESS_MESSAGE = (By.XPATH, "//ul[@class='messages']//li[contains(text(), 'Thank you')]")
    
    # 2. 订单号标题: "Order #25158..."
    ORDER_ID_HEADER = (By.XPATH, "//table//th[starts-with(text(), 'Order #')]")
    
    # 3. 返回主页链接
    RETURN_HOME_LINK = (By.LINK_TEXT, "Return to Main Menu")

    def is_order_submitted(self):
        """
        验证订单是否提交成功
        :return: True if success message is visible
        """
        return self.find_element(self.SUCCESS_MESSAGE)

    def get_order_id(self):
        """
        提取订单号
        :return: 订单号字符串 (例如: Order #25158 2026/07/21...)
        """
        text = self.get_text(self.ORDER_ID_HEADER)
        # 简单的清洗逻辑，只保留 Order #xxxxx 部分（可选）
        return text.split()[0] + " " + text.split()[1] if text else None

    def go_to_home(self):
        """点击返回主页"""
        self.click(self.RETURN_HOME_LINK)
        from pages.home_page import HomePage  # 避免循环导入，建议在这里导入
        return HomePage(self.driver)
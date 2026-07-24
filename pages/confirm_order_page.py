# pages/confirm_order_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.confirmation_page import ConfirmationPage

class ConfirmOrderPage(BasePage):
    """对应截图中的 'Please confirm the information below...' 页面"""
    
    # 定位器：根据截图，按钮文本是 "Confirm"
    CONFIRM_BUTTON = (By.LINK_TEXT, "Confirm")
    
    def is_loaded(self):
        """验证是否成功进入确认页"""
        return self.find_element(self.CONFIRM_BUTTON)

    def click_confirm(self):
        """点击 Confirm 按钮提交订单"""
        self.click(self.CONFIRM_BUTTON)
        return ConfirmationPage(self.driver)
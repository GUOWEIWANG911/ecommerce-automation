# pages/confirm_order_page.py
from pages.base_page import BasePage
from pages.confirmation_page import ConfirmationPage

class ConfirmOrderPage(BasePage):
    """对应 'Please confirm the information below...' 页面"""

    # 使用语义化定位器，比 LINK_TEXT 更稳定
    CONFIRM_BUTTON = "a:has-text('Confirm')"

    def is_loaded(self) -> bool:
        """验证是否成功进入确认页"""
        return self.is_visible(self.CONFIRM_BUTTON)


    def click_confirm(self) -> ConfirmationPage:
        """点击 Confirm 按钮提交订单"""
        self.click(self.CONFIRM_BUTTON)
        return ConfirmationPage(self.page)



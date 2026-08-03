# pages/checkout_page.py
from pages.base_page import BasePage
from pages.confirm_order_page import ConfirmOrderPage

class CheckoutPage(BasePage):

    # 支付信息：
    CARD_TYPE_SELECT = "select[name='order.cardType']"
    CARD_NUMBER_INPUT = "input[name='order.creditCard']"
    EXPIRY_DATE_INPUT = "input[name='order.expiryDate']"
    
    # 账单地址
    FIRST_NAME_INPUT = "input[name='order.billToFirstName']"
    LAST_NAME_INPUT = "input[name='order.billToLastName']"
    ADDRESS1_INPUT = "input[name='order.billAddress1']"
    CITY_INPUT = "input[name='order.billCity']"
    STATE_INPUT = "input[name='order.billState']"
    ZIP_INPUT = "input[name='order.billZip']"
    COUNTRY_INPUT = "input[name='order.billCountry']"

    # 提交按钮
    CONTINUE_BUTTON = "input[name='newOrder']"
    
    # 页面标题验证
    CHECKOUT_TITLE = "th:has-text('Payment Details')"

    def is_loaded(self) -> bool:
        """验证页面是否加载"""
        return self.page.locator(self.CHECKOUT_TITLE).is_visible()


    def fill_payment_info(self, card_type="Visa", card_number="9999 9999 9999 9999", expiry_date="12/30"):
        """填写支付信息"""
        self.page.locator(self.CARD_TYPE_SELECT).select_option(card_type)
        self.page.locator(self.CARD_NUMBER_INPUT).fill(card_number)
        self.page.locator(self.EXPIRY_DATE_INPUT).fill(expiry_date)


    def fill_billing_address(self, first_name="Test", last_name="User", 
                             address1="123 Main St", city="Beijing", 
                             state="BJ", zip_code="100000", country="China"):
        """填写账单地址"""
        self.page.locator(self.FIRST_NAME_INPUT).fill(first_name)
        self.page.locator(self.LAST_NAME_INPUT).fill(last_name)
        self.page.locator(self.ADDRESS1_INPUT).fill(address1)
        self.page.locator(self.CITY_INPUT).fill(city)
        self.page.locator(self.STATE_INPUT).fill(state)
        self.page.locator(self.ZIP_INPUT).fill(zip_code)
        self.page.locator(self.COUNTRY_INPUT).fill(country)


    def click_continue(self) -> ConfirmOrderPage:
        """点击继续按钮进入确认页"""
        self.page.locator(self.CONTINUE_BUTTON).click()
        return ConfirmOrderPage(self.page)



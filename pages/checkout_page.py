from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.confirmation_page import ConfirmationPage
from pages.confirm_order_page import ConfirmOrderPage

class CheckoutPage(BasePage):
    # --- 元素定位器 ---
    
    # 页面标题验证
    CHECKOUT_TITLE = (By.XPATH, "//table//th[contains(text(), 'Payment')]")

    # 支付信息
    CARD_TYPE_DROPDOWN = (By.NAME, "order.creditCard")
    CARD_NUMBER_INPUT = (By.NAME, "order.creditCard")
    EXPIRY_DATE_INPUT = (By.NAME, "order.expiryDate")
    
    # 账单地址
    FIRST_NAME_INPUT = (By.NAME, "order.billToFirstName")
    LAST_NAME_INPUT = (By.NAME, "order.billToLastName")
    ADDRESS1_INPUT = (By.NAME, "order.billAddress1")
    CITY_INPUT = (By.NAME, "order.billCity")
    STATE_INPUT = (By.NAME, "order.billState")
    ZIP_INPUT = (By.NAME, "order.billZip")
    COUNTRY_INPUT = (By.NAME, "order.billCountry")
    
    # 提交按钮
    CONTINUE_BUTTON = (By.NAME, "newOrder")

    def is_loaded(self):
        """验证页面是否加载"""
        return self.find_element(self.CHECKOUT_TITLE)
    
    def fill_payment_info(self, card_type="Visa", card_number="9999 9999 9999 9999", expiry_date="12/30"):
        """填写支付信息"""
        self.input_text(self.CARD_TYPE_DROPDOWN, card_type)
        self.input_text(self.CARD_NUMBER_INPUT, card_number)
        self.input_text(self.EXPIRY_DATE_INPUT, expiry_date)

    def fill_billing_address(self, first_name="Test", last_name="User", 
                             address1="123 Main St", city="Beijing", 
                             state="BJ", zip_code="100000", country="China"):
        """填写账单地址"""
        self.input_text(self.FIRST_NAME_INPUT, first_name)
        self.input_text(self.LAST_NAME_INPUT, last_name)
        self.input_text(self.ADDRESS1_INPUT, address1)
        self.input_text(self.CITY_INPUT, city)
        self.input_text(self.STATE_INPUT, state)
        self.input_text(self.ZIP_INPUT, zip_code)
        self.input_text(self.COUNTRY_INPUT, country)

    def click_continue(self):
        """点击继续按钮进入确认页"""
        self.click(self.CONTINUE_BUTTON)
        return ConfirmOrderPage(self.driver)  # 假设你接下来会创建确认页

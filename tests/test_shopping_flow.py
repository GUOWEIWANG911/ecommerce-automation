# tests/test_shopping_flow.py
import yaml
import unittest
from ddt import ddt, data, unpack
from selenium import webdriver
from utils.config import BASE_URL, USERNAME, PASSWORD, SEARCH_KEYWORD
from pages.login_page import LoginPage

with open('test_data.yaml', 'r', encoding='utf-8') as f:
    GLOBAL_TEST_DATA = yaml.safe_load(f)

@ddt
class TestShoppingFlow(unittest.TestCase):

    @classmethod
    def setupClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.test_data = GLOBAL_TEST_DATA

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(f"{BASE_URL}/actions/Catalog.action")

    @data(*GLOBAL_TEST_DATA['login_cases'])
    @unpack
    def test_login_with_multiple_accounts(self, username, password, expected_title):
        """数据驱动测试，验证多组账号登录"""
        driver = self.driver
        login_page = LoginPage(driver)
        login_page.click_sign_in_link()

        # 使用传入的参数进行登录
        home_page = login_page.login(username, password)

        # 看标题是否符合预期
        self.assertIn(expected_title, driver.title)

    def test_complete_purchase_flow(self):
        driver = self.driver

        """测试完整的登录、搜索、下单流程"""
        # 1. 登录(这里可以取第一组账号，或者单独指定一个测试账号)
        login_page = LoginPage(driver)
        login_page.click_sign_in_link()  # 先点击跳转
        # 使用数据文件中的第一个账号
        test_user = GLOBAL_TEST_DATA['login_cases'][0]
        home_page = login_page.login(test_user['username'], test_user['password'])

        # 2. 搜索商品并进入详情
        cart_page = home_page.search_product(SEARCH_KEYWORD).click_first_product().add_to_cart()

        # 3. 断言：验证是否成功进入购物车页面
        self.assertTrue(cart_page.is_cart_page_loaded(), "购物车页面未成功加载")

        # 4. 从购物车进入结算页面
        checkout_page = cart_page.go_to_checkout()
        self.assertTrue(checkout_page.is_loaded(), "结算页面未成功加载")

        # 5. 填写支付信息(从 YAML 读取)
        order_info = GLOBAL_TEST_DATA['order_info']
        checkout_page.fill_payment_info(
            card_type=order_info['card_type'],
            card_number=order_info['card_number'],
            expiry_date=order_info['expiry_date']
        )

        # 6. 填写账单地址（从 YAML 读取）
        checkout_page.fill_billing_address(
            first_name=order_info['first_name'],
            last_name=order_info['last_name'],
            address1=order_info['address1'],
            city=order_info['city'],
            state=order_info['state'],
            zip_code=order_info['zip_code'],
            country=order_info['country']
        )
        
        # 7. 点击提交订单按钮
        confirm_order_page = checkout_page.click_continue()
        self.assertTrue(confirm_order_page.is_loaded(), "确认订单页未加载")

        confirmation_page = confirm_order_page.click_confirm()
        
        # 8. 额外断言：验证获取到了订单号
        order_id = confirmation_page.get_order_id()
        self.assertIsNotNone(order_id, "未能获取到订单号")
        print(f"✅ 测试通过！生成的订单号为: {order_id}")

    def tearDown(self):
        self.driver.quit()
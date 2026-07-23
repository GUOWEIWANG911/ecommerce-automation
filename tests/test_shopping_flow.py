# tests/test_shopping_flow.py
import pytest
from utils.config import BASE_URL, SEARCH_KEYWORD
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from conftest import load_login_cases

class TestShoppingFlow:

    @pytest.mark.parametrize(
        "username, password, expected_title",
        [
            (case['username'], case['password'], case['expected_title'])
            for case in load_login_cases()
        ],
        ids=[case['username'] for case in load_login_cases()]
    )
    def test_login_with_multiple_accounts(self, driver, username, password, expected_title):
        """数据驱动测试，验证多组账号登录"""
        # 1. 访问首页
        driver.get(f"{BASE_URL}/actions/Catalog.action")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # 2. 状态清理：如果已登录，先退出
        try:
            driver.find_element(By.LINK_TEXT, "Sign Out").click()
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Sign In"))
            )
        except NoSuchElementException:
            pass

        # 3. 登录
        login_page = LoginPage(driver)
        login_page.click_sign_in_link()
        home_page = login_page.login(username, password)

        # 4. 断言
        assert expected_title in driver.title, \
            f"登录失败，期望标题包含 '{expected_title}'，实际标题: {driver.title}"

    @pytest.mark.usefixtures("driver")
    def test_complete_purchase_flow(self, driver, global_test_data):
        """测试完整的登录、搜索、下单流程"""
        driver.get(f"{BASE_URL}/actions/Catalog.action")
        driver.set_window_size(1920, 1080)

        # 如果上一个测试没退出，这里先退出
        from selenium.common.exceptions import NoSuchElementException
        try:
            driver.find_element(By.LINK_TEXT, "Sign Out").click()
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Sign In"))
            )
        except NoSuchElementException:
            pass  # 本来就是未登录状态，不用管
        
        # 1. 登录 - 从 fixture 获取数据
        login_page = LoginPage(driver)
        login_page.click_sign_in_link()
        test_user = global_test_data['login_cases'][0]
        home_page = login_page.login(test_user['username'], test_user['password'])

        # 2. 搜索商品并进入详情
        cart_page = home_page.search_product(SEARCH_KEYWORD).click_first_product().add_to_cart()
        assert cart_page.is_cart_page_loaded(), "购物车页面未成功加载"

        # 3. 进入结算页面
        checkout_page = cart_page.go_to_checkout()
        assert checkout_page.is_loaded(), "结算页面未成功加载"

        # 4. 填写支付与账单信息 - 从 fixture 获取数据
        order_info = global_test_data['order_info']
        checkout_page.fill_payment_info(
            card_type=order_info['card_type'],
            card_number=order_info['card_number'],
            expiry_date=order_info['expiry_date']
        )
        checkout_page.fill_billing_address(
            first_name=order_info['first_name'],
            last_name=order_info['last_name'],
            address1=order_info['address1'],
            city=order_info['city'],
            state=order_info['state'],
            zip_code=order_info['zip_code'],
            country=order_info['country']
        )
        
        # 5. 提交订单并验证
        confirm_order_page = checkout_page.click_continue()
        assert confirm_order_page.is_loaded(), "确认订单页未加载"
        
        confirmation_page = confirm_order_page.click_confirm()
        order_id = confirmation_page.get_order_id()
        assert order_id is not None, "未能获取到订单号"
        print(f"✅ 测试通过！生成的订单号为: {order_id}")

# import sys
# import platform
# import yaml
# import unittest
# from ddt import ddt, data, unpack
# from selenium import webdriver
# from utils.config import BASE_URL, USERNAME, PASSWORD, SEARCH_KEYWORD
# from pages.login_page import LoginPage
# from selenium.webdriver.chrome.options import Options

# with open('test_data.yaml', 'r', encoding='utf-8') as f:
#     GLOBAL_TEST_DATA = yaml.safe_load(f)

# @ddt
# class TestShoppingFlow(unittest.TestCase):

#     @classmethod
#     # def setUpClass(cls):
#     #     # 1. 创建 Options 对象
#     #     chrome_options = Options()
#     #     # 2. 指定 Chrome 浏览器的二进制文件路径
#     #     chrome_options.binary_location = "/usr/bin/google-chrome"

#     #     # 3. 添加在 Docker 环境中运行所必需的参数
#     #     chrome_options.add_argument("--headless") # 无头模式，不显示浏览器界面
#     #     chrome_options.add_argument("--no-sandbox") # 解决DevToolsActivePort文件不存在的报错
#     #     chrome_options.add_argument("--disable-dev-shm-usage") # 克服共享内存不足的问题

#     #     # 4. 将 options 传递给 webdriver
#     #     cls.driver = webdriver.Chrome(options=chrome_options)
        
#     #     cls.driver.maximize_window()
#     #     cls.test_data = GLOBAL_TEST_DATA

#     def setUp(self):
#         # ✅ 不要在这里 new driver！直接使用 conftest 传进来的 self.driver
#         # 假设你已经通过某种方式（如 BasePage 或 fixture 注入）获取了 driver
        
#         # 1. 设置窗口大小 (虽然 conftest 里设了，但这里设也没坏处)
#         self.driver.set_window_size(1920, 1080)
        
#         # 2. 访问首页
#         self.driver.get(f"{BASE_URL}/actions/Catalog.action")
        
#         # 3. 可选：清理缓存 (如果需要的话)
#         # self.driver.delete_all_cookies()

#     @data(*GLOBAL_TEST_DATA['login_cases'])
#     @unpack
#     def test_login_with_multiple_accounts(self, username, password, expected_title):
#         """数据驱动测试，验证多组账号登录"""
#         driver = self.driver
#         login_page = LoginPage(driver)
#         login_page.click_sign_in_link()

#         # 使用传入的参数进行登录
#         home_page = login_page.login(username, password)

#         # 看标题是否符合预期
#         self.assertIn(expected_title, driver.title)

#     def test_complete_purchase_flow(self):
#         driver = self.driver
#         self.driver.set_window_size(1920, 1080)

#         """测试完整的登录、搜索、下单流程"""
#         # 1. 登录(这里可以取第一组账号，或者单独指定一个测试账号)
#         login_page = LoginPage(driver)
#         login_page.click_sign_in_link()  # 先点击跳转
#         # 使用数据文件中的第一个账号
#         test_user = GLOBAL_TEST_DATA['login_cases'][0]
#         home_page = login_page.login(test_user['username'], test_user['password'])

#         # 2. 搜索商品并进入详情
#         cart_page = home_page.search_product(SEARCH_KEYWORD).click_first_product().add_to_cart()

#         # 3. 断言：验证是否成功进入购物车页面
#         self.assertTrue(cart_page.is_cart_page_loaded(), "购物车页面未成功加载")

#         # 4. 从购物车进入结算页面
#         checkout_page = cart_page.go_to_checkout()
#         self.assertTrue(checkout_page.is_loaded(), "结算页面未成功加载")

#         # 5. 填写支付信息(从 YAML 读取)
#         order_info = GLOBAL_TEST_DATA['order_info']
#         checkout_page.fill_payment_info(
#             card_type=order_info['card_type'],
#             card_number=order_info['card_number'],
#             expiry_date=order_info['expiry_date']
#         )

#         # 6. 填写账单地址（从 YAML 读取）
#         checkout_page.fill_billing_address(
#             first_name=order_info['first_name'],
#             last_name=order_info['last_name'],
#             address1=order_info['address1'],
#             city=order_info['city'],
#             state=order_info['state'],
#             zip_code=order_info['zip_code'],
#             country=order_info['country']
#         )
        
#         # 7. 点击提交订单按钮
#         confirm_order_page = checkout_page.click_continue()
#         self.assertTrue(confirm_order_page.is_loaded(), "确认订单页未加载")

#         confirmation_page = confirm_order_page.click_confirm()
        
#         # 8. 额外断言：验证获取到了订单号
#         order_id = confirmation_page.get_order_id()
#         self.assertIsNotNone(order_id, "未能获取到订单号")
#         print(f"✅ 测试通过！生成的订单号为: {order_id}")

#     def tearDown(self):
#         if self.driver:
#             try:
#                 self.driver.delete_all_cookies()
#             except Exception:
#                 pass  # 如果 driver 已经断开，忽略错误

#         self.driver.quit()
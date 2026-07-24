# tests/test_shopping_flow.py
import pytest
from utils.config import BASE_URL, SEARCH_KEYWORD
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException
)
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
            sign_out_link = driver.find_element(By.LINK_TEXT, "Sign Out")
            sign_out_link.click()
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Sign In"))
            )
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
            pass

        # 3. 登录
        login_page = LoginPage(driver)
        login_page.click_sign_in_link()
        home_page = login_page.login(username, password)

        # 4. 断言
        assert expected_title in driver.title, \
            f"登录失败，期望标题包含 '{expected_title}'，实际标题: {driver.title}"

        # 5. 每次登录测试结束后，主动登出，为下一个账号/测试用例准备干净环境
        try:
            sign_out_link = driver.find_element(By.LINK_TEXT, "Sign Out")
            sign_out_link.click()
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Sign In"))
            )
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
            print(f"账号 {username} 登出失败，可能影响后续测试")

    @pytest.mark.usefixtures("driver")
    def test_complete_purchase_flow(self, driver, global_test_data):
        """测试完整的登录、搜索、下单流程"""
        driver.get(f"{BASE_URL}/actions/Catalog.action")
        driver.set_window_size(1920, 1080)

        # 0. 增强版状态清理：确保回到未登录的首页状态
        try:
            # 尝试找“退出”链接，如果找到说明是登录状态
            sign_out_link = driver.find_element(By.LINK_TEXT, "Sign Out")
            sign_out_link.click()
            # 点击后，等待“登录”链接出现，确认已退出并回到首页
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Sign In"))
            )
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
            # 如果找不到“退出”链接，说明可能已经是未登录状态
            # 但为了确保万无一失，我们再检查一次是否在首页
            # 如果不在首页（比如还在购物车页），就重新加载一次首页
            try:
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Sign In"))
                )
            except TimeoutException:
                # 如果等了3秒还没看到“Sign In”，说明页面不对，强制刷新
                driver.get(f"{BASE_URL}/actions/Catalog.action")
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "Sign In"))
                )
            # 如果找到了“Sign In”，说明状态正确，直接pass
            pass
        
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

        # 测试结束后主动登出，保持环境干净
        try:
            sign_out_link = driver.find_element(By.LINK_TEXT, "Sign Out")
            sign_out_link.click()
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Sign In"))
            )
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
            print("⚠️ 完整流程测试登出失败")

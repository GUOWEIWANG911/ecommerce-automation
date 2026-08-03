# tests/test_shopping_flow.py
import pytest
from utils.config import BASE_URL, SEARCH_KEYWORD
from pages.login_page import LoginPage
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
    def test_login_with_multiple_accounts(self, page, username, password, expected_title):
        """数据驱动测试，验证多组账号登录"""
        # 1. 访问首页（Playwright 的 goto 自带等待，无需 WebDriverWait）
        page.goto(f"{BASE_URL}/actions/Catalog.action")

        # 2. 状态清理（关键修改点）
        # 情况 A: 如果看到 "Sign Out"，说明已登录，点击退出
        sign_out_link = page.locator("a:has-text('Sign Out')")
        if sign_out_link.is_visible():
            sign_out_link.click()
            # 退出后通常会回到首页，等待 "Sign In" 出现
            page.locator("a:has-text('Sign In')").wait_for()

        # 情况 B: 如果看到 "Username" 输入框，说明已经在登录页了，不需要再点击 "Sign In"
        # 注意：这里使用 input[name='username'] 或其他登录页特有的元素
        username_input = page.locator("input[name='username']")
        
        login_page = LoginPage(page)
        
        # 只有当不在登录页时，才点击 "Sign In" 链接
        if not username_input.is_visible():
            login_page.click_sign_in_link()
        
        # 3. 执行登录
        home_page = login_page.login(username, password)

        # 4. 断言
        assert expected_title in page.title(), \
            f"登录失败，期望标题包含 '{expected_title}'，实际标题: {page.title}"

        # 5. 登出：Playwright 的 click 自带重试，无需异常捕获
        sign_out_link = page.locator("a:has-text('Sign Out')")
        if sign_out_link.is_visible():
            sign_out_link.click()
            page.locator("a:has-text('Sign In')").wait_for()

    def test_complete_purchase_flow(self, page, global_test_data):
        """测试完整的登录、搜索、下单流程"""
        page.goto(f"{BASE_URL}/actions/Catalog.action")
        page.set_viewport_size({"width": 1920, "height": 1080})

        # --- 状态清理开始 ---
        sign_out_link = page.locator("a:has-text('Sign Out')")
        if sign_out_link.is_visible():
            sign_out_link.click()
            page.locator("a:has-text('Sign In')").wait_for()

        # 检查是否已经在登录页
        if not page.locator("input[name='username']").is_visible():
            login_page = LoginPage(page)
            login_page.click_sign_in_link()
        else:
            login_page = LoginPage(page)
        # --- 状态清理结束 ---

        test_user = global_test_data['login_cases'][0]
        home_page = login_page.login(test_user['username'], test_user['password'])

        # 2. 搜索商品并进入详情（链式调用，Playwright 自动等待页面跳转）
        cart_page = home_page.search_product(SEARCH_KEYWORD).click_first_product().add_to_cart()
        assert cart_page.is_cart_visible(), "购物车页面未成功加载"

        # 3. 进入结算页面
        checkout_page = cart_page.proceed_to_checkout()
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

        # 登出：Playwright 的 click 自带重试，无需异常捕获
        sign_out_link = page.locator("a:has-text('Sign Out')")
        if sign_out_link.is_visible():
            sign_out_link.click()
            page.locator("a:has-text('Sign In')").wait_for()
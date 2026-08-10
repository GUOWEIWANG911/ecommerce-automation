# tests/test_shopping_flow.py
import pytest
from utils.config import BASE_URL, SEARCH_KEYWORD
from pages.login_page import LoginPage
from conftest import load_login_cases
from playwright.sync_api import expect
from playwright.sync_api import Error as PlaywrightError

class TestShoppingFlow:

    @pytest.mark.parametrize(
        "username, password, expected_title",
        [
            (case['username'], case['password'], case['expected_title'])
            for case in load_login_cases()
        ],
        ids=[case['username'] for case in load_login_cases()]
    )
    def test_login_with_multiple_accounts(self, page, ensure_login_page, username, password, expected_title):
        """数据驱动测试，验证多组账号登录"""
        # 1. 统一清理 + 获取 LoginPage（仅 1 行）
        login_page = ensure_login_page()
        
        # 2. 执行登录
        home_page = login_page.login(username, password)

        # 3. 断言
        assert expected_title in page.title(), \
            f"登录失败，期望标题包含 '{expected_title}'，实际标题: {page.title}"


    def test_login_with_new_user(self, page, new_user, ensure_login_page):
        """测试使用刚刚自动注册的新用户登录"""

        # 1. 统一清理 + 获取 LoginPage
        login_page = ensure_login_page()

        # 2. 登录
        home_page = login_page.login(new_user["username"], new_user["password"])

        # 3. 断言
        expect(page.locator("a:has-text('Sign Out')")).to_be_visible(timeout=5000)


    def test_complete_purchase_flow(self, page, ensure_login_page, global_test_data):
        """测试完整的登录、搜索、下单流程"""
        # 1. 统一清理 + 获取 LoginPage
        login_page = ensure_login_page()

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
        print(f"测试通过！生成的订单号为: {order_id}")


    def test_mock_out_of_stock(self, page, new_user, ensure_login_page):
        """使用 page.route 模拟商品缺货"""
        # 1. 设置路由拦截：拦截商品详情页请求
        def handle_product_route(route):
            # 返回一个伪造的 HTML 页面
            fake_html = """
            <html><body>
                <div id="Catalog">
                    <h2>Item: EST-1</2>
                    <p class="error">Sorry, this item is currently OUT OF STOCK!</p>
                </div>
            </body></html>
            """
            route.fulfill(status=200, content_type="text/html", body=fake_html)

        page.route("**/Catalog.action?viewProduct=*", handle_product_route)

        # 2. 执行正常的页面操作
        login_page = ensure_login_page()
        home_page = login_page.login(new_user["username"], new_user["password"])
        cart_page = home_page.search_product(SEARCH_KEYWORD).click_first_product()

        expect(page.locator("p.error")).to_contain_text("OUT OF STOCK")


    def test_network_timeout(self, page):
    # 拦截所有请求，模拟网络断开
        page.route("**/*", lambda route: route.abort())

        with pytest.raises(PlaywrightError) as exc_info:
            page.goto(f"{BASE_URL}/actions/Catalog.action")

        assert "page.goto" in str(exc_info.value)

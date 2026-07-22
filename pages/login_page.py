#pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.home_page import HomePage

class LoginPage(BasePage):
    # JPetStore 登录页元素定位器
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BUTTON = (By.NAME, "signon")

    # 首页上的 Sign In 链接定位器
    SIGN_IN_LINK = (By.PARTIAL_LINK_TEXT, "Sign In")

    def click_sign_in_link(self):
        """点击首页的 Sign In 链接"""
        self.find_element(self.SIGN_IN_LINK).click()

        WebDriverWait(self.driver, 10).until(
            lambda d: "Account.action" in d.current_url
        )

    def login(self, username, password):
        """封装登录业务"""
        # 1. 输入用户名和密码
        self.input_text(self.USERNAME_INPUT, username)
        self.input_text(self.PASSWORD_INPUT, password)
        
        # 2. 点击登录按钮
        self.find_element(self.LOGIN_BUTTON).click()

        # 3. 登录成功后跳转回首页，返回 HomePage 对象供后续步骤使用
        self.default_wait.until(EC.url_contains("Catalog.action"))
        return HomePage(self.driver)
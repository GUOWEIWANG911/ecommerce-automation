# pages/login_page.py
from pages.base_page import BasePage
from pages.home_page import HomePage

class LoginPage(BasePage):
    # 语义化定位器
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    SIGN_IN_BUTTON = "input[name='signon']"
    SIGN_IN_LINK = "a:has-text('Sign In')"

    def click_sign_in_link(self) -> "LoginPage":
        """点击首页的 Sign In 链接"""
        self.click(self.SIGN_IN_LINK)
        return self


    def login(self, username: str, password: str) -> HomePage:
        """执行登录，返回 HomePage"""
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.SIGN_IN_BUTTON)
        return HomePage(self.page)


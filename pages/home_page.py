#pages/home_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.product_page import ProductPage

class HomePage(BasePage):
    # JPetStore 首页/搜索结果页元素定位器
    SEARCH_BOX = (By.NAME, "keyword")
    SEARCH_BUTTON = (By.NAME, "searchProducts")
    FIRST_PRODUCT_LINK = (By.CSS_SELECTOR, "#Catalog a") # 搜索"dog"后的第一个商品

    def search_product(self, keyword):
        # self.input_text(self.SEARCH_BOX, keyword)
        # # self.click(self.SEARCH_BUTTON)
        # # btn = self.find_element(self.SEARCH_BUTTON)
        # # self.driver.execute_script("arguments[0].click();", btn)
        # return self
        search_box = self.find_element(self.SEARCH_BOX)
        search_box.clear()
        search_box.send_keys(keyword)
        
        # ✅ 核心修改：直接发送回车键，模拟用户操作
        # 这比 click() 和 submit() 都更可靠，能强制触发表单提交
        self.click(self.SEARCH_BUTTON)
        
        return self

    def click_first_product(self):
        # 🔍 调试代码：打印当前 URL 和页面标题
        print(f"[DEBUG] Current URL: {self.driver.current_url}")
        print(f"[DEBUG] Page Title: {self.driver.title}")
        
        # 🔍 调试代码：打印页面源码的前 2000 个字符
        print(f"[DEBUG] Page Source (first 2000 chars): {self.driver.page_source[:2000]}")
        
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.element_to_be_clickable(self.FIRST_PRODUCT_LINK))
        
        self.click(self.FIRST_PRODUCT_LINK)
        return ProductPage(self.driver)

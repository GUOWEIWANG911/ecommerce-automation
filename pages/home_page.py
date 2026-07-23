#pages/home_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.product_page import ProductPage
from selenium.common.exceptions import TimeoutException

class HomePage(BasePage):
    # JPetStore 首页/搜索结果页元素定位器
    SEARCH_BOX = (By.NAME, "keyword")
    SEARCH_BUTTON = (By.NAME, "searchProducts")
    FIRST_PRODUCT_LINK = (By.CSS_SELECTOR, "#Catalog b a") # 搜索"dog"后的第一个商品

    def search_product(self, keyword):
        self.input_text(self.SEARCH_BOX, keyword)
        self.click(self.SEARCH_BUTTON)

        # --- 优化后的等待逻辑 ---
        wait = WebDriverWait(self.driver, 20) # 将等待时间延长到20秒
        
        try:
            # 策略1：首选等待首页的 "Welcome" 标志消失
            wait.until(EC.invisibility_of_element_located((By.ID, "Welcome")))
        except TimeoutException:
            # 策略2：如果等待消失超时，作为备选，检查是否已经跳转到了结果页
            # 我们等待结果页的某个特征出现，比如 "Products" 标题
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Products')]")))
            except TimeoutException:
                # 如果两个策略都失败了，再抛出异常，并附上调试信息
                print(f"[DEBUG] 搜索后页面未跳转。当前URL: {self.driver.current_url}")
                print(f"[DEBUG] 页面标题: {self.driver.title}")
                raise

        return self

    def click_first_product(self):
        # 🔍 调试代码：打印当前 URL 和页面标题
        print(f"[DEBUG] Current URL: {self.driver.current_url}")
        print(f"[DEBUG] Page Title: {self.driver.title}")
        
        # # 🔍 调试代码：打印页面源码的前 5000 个字符
        # print(f"[DEBUG] Page Source (first 5000 chars): {self.driver.page_source[:5000]}")
        try:
            content_div = self.driver.find_element(By.CSS_SELECTOR, "div#Content")
            print(f"[DEBUG] 商品列表容器 (div#Content) 的HTML内容:\n{content_div.get_attribute('innerHTML')}")
        except Exception as e:
            print(f"[DEBUG] 未能找到商品列表容器 div#Content: {e}")
        
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.element_to_be_clickable(self.FIRST_PRODUCT_LINK))
        
        self.click(self.FIRST_PRODUCT_LINK)
        return ProductPage(self.driver)

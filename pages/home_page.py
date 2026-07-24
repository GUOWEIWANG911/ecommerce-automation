#pages/home_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.product_page import ProductPage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

class HomePage(BasePage):
    # JPetStore 首页/搜索结果页元素定位器
    SEARCH_BOX = (By.NAME, "keyword")
    SEARCH_BUTTON = (By.NAME, "searchProducts")
    # FIRST_PRODUCT_LINK = (By.CSS_SELECTOR, "#Catalog b a") # 搜索"dog"后的第一个商品
    # FIRST_PRODUCT_LINK = (By.XPATH, "//div[@id='Catalog']//a[contains(@href, 'productId=') and .//img]")

    def search_product(self, keyword):

        # 1. 找到搜索框
        search_box = self.driver.find_element(*self.SEARCH_BOX)
        # 2. 清空搜索框（以防万一）
        search_box.clear()
        # 3. 输入关键词并按下回车键
        search_box.send_keys(keyword + Keys.RETURN)

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
        
        # # # 🔍 调试代码：打印页面源码的前 5000 个字符
        # # print(f"[DEBUG] Page Source (first 5000 chars): {self.driver.page_source[:5000]}")
        # try:
        #     content_div = self.driver.find_element(By.CSS_SELECTOR, "div#Content")
        #     print(f"[DEBUG] 商品列表容器 (div#Content) 的HTML内容:\n{content_div.get_attribute('innerHTML')}")
        # except Exception as e:
        #     print(f"[DEBUG] 未能找到商品列表容器 div#Content: {e}")

        first_product_link_xpath = "//div[@id='Catalog']//a[contains(@href, 'productId=') and .//img]"

        wait = WebDriverWait(self.driver, 15)
        link = wait.until(EC.element_to_be_clickable((By.XPATH, first_product_link_xpath)))
        link.click()
        
        # 【新增】显式等待页面跳转完成
        # 详情页的 URL 会包含 "viewProduct"
        wait.until(lambda d: "viewProduct" in d.current_url)
        
        # 可选：再等一个详情页特有的元素，双重保险
        # wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2"))) 
        
        print(f"[DEBUG] 已跳转到详情页, 新URL: {self.driver.current_url}")
        return ProductPage(self.driver)
        
        # wait = WebDriverWait(self.driver, 15)
        # wait.until(EC.element_to_be_clickable(self.FIRST_PRODUCT_LINK))
        
        # # self.click(self.FIRST_PRODUCT_LINK)
        # self.driver.find_element(*FIRST_PRODUCT_LINK).click()


        # # 【修改点2】关键！等待页面跳转到商品详情页
        # # 商品详情页的特征是有一个 "Add to Cart" 按钮，我们等待它出现
        # # 这比等待URL变化更可靠
        # try:
        #     wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Add to Cart")))
        # except TimeoutException:
        #     # 如果等待超时，打印调试信息
        #     print(f"[DEBUG] 页面跳转失败！当前URL: {self.driver.current_url}")
        #     print(f"[DEBUG] 页面标题: {self.driver.title}")
        #     raise

        # # 确认跳转成功后，再返回 ProductPage 对象
        # return ProductPage(self.driver)

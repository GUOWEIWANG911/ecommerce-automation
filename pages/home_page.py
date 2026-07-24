#pages/home_page.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.product_page import ProductPage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from .search_results_page import SearchResultsPage

class HomePage(BasePage):
    # JPetStore 首页/搜索结果页元素定位器
    SEARCH_BOX = (By.NAME, "keyword")
    # SEARCH_BUTTON = (By.NAME, "searchProducts")
    # FIRST_PRODUCT_LINK = (By.CSS_SELECTOR, "#Catalog b a") # 搜索"dog"后的第一个商品
    # FIRST_PRODUCT_LINK = (By.XPATH, "//div[@id='Catalog']//a[contains(@href, 'productId=') and .//img]")
    SEARCH_BUTTON = (By.XPATH, "//input[@type='submit' and @value='Search']")
    SEARCH_RESULT_HEADER = (By.XPATH, "//th[contains(text(), 'Product ID')]")
    # 
    def search_product(self, keyword):
        search_box = self.driver.find_element(By.NAME, "keyword")
        search_box.send_keys(keyword)
        
        # --- 修改开始 ---
        # 找到搜索按钮并点击它，而不是用 Keys.RETURN
        search_button = self.driver.find_element(By.NAME, "searchProducts")
        search_button.click()
        # --- 修改结束 ---

        # # 等待搜索结果页加载
        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[@id='Catalog']//h4"))
        # )

        time.sleep(3)
    
        # 2. 打印当前页面的标题和URL
        print(f"\n[DEBUG] 当前页面标题: {self.driver.title}")
        print(f"[DEBUG] 当前页面URL: {self.driver.current_url}")
        
        # 3. 打印整个页面的源代码，这是最关键的一步！
        print(f"[DEBUG] 当前页面源代码:\n{self.driver.page_source}\n")

        return SearchResultsPage(self.driver)
    
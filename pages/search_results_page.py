# pages/search_results_page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .product_page import ProductPage

class SearchResultsPage:
    def __init__(self, driver):
        self.driver = driver

    def click_first_product(self):
        """
        在搜索结果页点击第一个商品
        """
        print(f"[DEBUG] 准备在搜索结果页点击第一个商品, 当前URL: {self.driver.current_url}")
        
        # --- 修改开始 ---
        # 修正定位器，匹配实际的HTML结构。
        # 商品链接在 <td> 标签内，而不是 <h4> 标签内。
        first_product_link = (By.XPATH, "//div[@id='Catalog']//tr[2]//td[1]/a[contains(@href, 'viewProduct')]")
        # --- 修改结束 ---
        
        wait = WebDriverWait(self.driver, 20)
        
        # 等待链接出现并可点击
        link = wait.until(EC.element_to_be_clickable(first_product_link))
        
        print(f"[DEBUG] 即将点击商品ID: {link.text}")
        link.click()
        
        # 等待页面跳转到商品详情页
        wait.until(lambda d: "viewProduct" in d.current_url)
        
        print(f"[DEBUG] 跳转成功: {self.driver.current_url}")
        return ProductPage(self.driver)
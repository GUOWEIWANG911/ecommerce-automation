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

        first_product_link = (By.XPATH, "//div[@id='Catalog']//tr[2]//td[1]/a[contains(@href, 'viewProduct')]")
        
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_element_located(first_product_link))
        
        # 等待链接出现并可点击
        link = wait.until(EC.element_to_be_clickable(first_product_link))
        link.click()

        print(f"[DEBUG] 点击后，当前页面URL: {self.driver.current_url}")
        print(f"[DEBUG] 点击后，当前页面标题: {self.driver.title}")
        
        # 等待页面跳转到商品详情页
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='Add to Cart']")))
        print(f"[DEBUG] 商品详情页已加载: {self.driver.current_url}")
        return ProductPage(self.driver)
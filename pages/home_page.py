#pages/home_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from .search_results_page import SearchResultsPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage(BasePage):
    # JPetStore 首页/搜索结果页元素定位器
    SEARCH_BOX = (By.NAME, "keyword")
    SEARCH_BUTTON = (By.XPATH, "//input[@type='submit' and @value='Search']")
    SEARCH_RESULT_HEADER = (By.XPATH, "//th[contains(text(), 'Product ID')]")

    def search_product(self, keyword):
        search_box = self.driver.find_element(By.NAME, "keyword")
        search_box.send_keys(keyword)
        
        # 找到搜索按钮并点击它，而不是用 Keys.RETURN
        search_button = self.driver.find_element(By.NAME, "searchProducts")
        search_button.click()

        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//th[contains(text(), 'Product ID')]"))
        )

        return SearchResultsPage(self.driver)
    
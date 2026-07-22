#pages/home_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.product_page import ProductPage

class HomePage(BasePage):
    # JPetStore 首页/搜索结果页元素定位器
    SEARCH_BOX = (By.NAME, "keyword")
    SEARCH_BUTTON = (By.NAME, "searchProducts")
    FIRST_PRODUCT_LINK = (By.CSS_SELECTOR, "a[href*='productid=']") # 搜索"dog"后的第一个商品

    def search_product(self, keyword):
        self.input_text(self.SEARCH_BOX, keyword)
        self.click(self.SEARCH_BUTTON)
        return self
    
    def click_first_product(self):
        self.click(self.FIRST_PRODUCT_LINK)
        return ProductPage(self.driver) # 进入商品详情页
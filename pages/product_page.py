# pages/product_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.cart_page import CartPage

class ProductPage(BasePage):
    # 1. 定义定位器常量
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "a[href*='workingItemId=EST-7']")

    def add_to_cart(self):
        """将商品加入购物车"""
        # 2. 把等待和点击逻辑放进方法里
        wait = WebDriverWait(self.driver, 20)
        
        # 先确认页面加载到了商品列表区域
        wait.until(EC.presence_of_element_located((By.ID, "Catalog")))
        
        # 再等待按钮可点击
        add_to_cart_btn = wait.until(
            EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON)
        )
        add_to_cart_btn.click()
        
        # 3. 返回购物车页面对象
        return CartPage(self.driver)
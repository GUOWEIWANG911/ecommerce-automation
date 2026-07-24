# pages/product_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.cart_page import CartPage

class ProductPage(BasePage):
    # 1. 定义定位器常量
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "a[href*='addItemToCart']")

    def add_to_cart(self):
        print(self.driver.current_url)

        # 🔍 调试：打印页面所有链接文本
        all_links = self.driver.find_elements(By.TAG_NAME, "a")
        link_texts = [link.text for link in all_links if link.text.strip()]
        print(f"[DEBUG] 页面所有链接文本: {link_texts}")

        """将商品加入购物车"""
        # 2. 把等待和点击逻辑放进方法里
        wait = WebDriverWait(self.driver, 30)
        
        # 先确认页面加载到了商品列表区域
        wait.until(EC.presence_of_element_located((By.ID, "Catalog")))
        
        # 再等待按钮可点击
        add_to_cart_btn = wait.until(
            EC.presence_of_element_located(self.ADD_TO_CART_BUTTON)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart_btn)
        add_to_cart_btn.click()
        
        # 3. 返回购物车页面对象
        return CartPage(self.driver)
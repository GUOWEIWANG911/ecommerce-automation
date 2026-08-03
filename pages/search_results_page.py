#pages/search_results_page.py
from pages.base_page import BasePage
from pages.product_page import ProductPage

class SearchResultsPage(BasePage):
    # 精确匹配商品连接，避免匹配到到导航栏
    FIRST_PRODUCT_LINK = "a[href*='productId=']"

    def click_first_product(self) -> ProductPage:
        # 1. 点击第一个商品连接
        # Playwright 会自动等待链接可见、可点击，且点击后页面跳转完成
        self.click(self.FIRST_PRODUCT_LINK)

        # 2. 返回商品详情页面
        # 注意: Playwright 的 click() 会自动等待页面加载完成
        # 不再需要 wait.until(EC.presence_of_element_located(...))
        return ProductPage(self.page)


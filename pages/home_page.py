#pages/home_page.py
from pages.base_page import BasePage
from pages.search_results_page import SearchResultsPage

class HomePage(BasePage):
    # Playwright 语义化定位器（比 XPath 更稳定）
    SEARCH_BOX = "input[name='keyword']"
    SEARCH_BUTTON = "input[name='searchProducts']"
    SEARCH_RESULT_HEADER = "th:has-text('Product ID')"

    def search_product(self, keyword: str) -> SearchResultsPage:
        # 1.  输入关键词（自动等待输入框可交互）
        self.fill(self.SEARCH_BOX, keyword)

        # 2. 点击搜索（自动等待按钮可点击，无需 JS 兜底）
        self.click(self.SEARCH_BUTTON)

        # 3. 等待搜索结果页加载（Playwright 自动等待，无需显示等待）
        # 注意： 这里不需要 wait.until(), 直接断言或返回即可
        # 因为下一步操作会自动等待元素出现
        return SearchResultsPage(self.page)


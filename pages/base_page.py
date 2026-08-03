# pages/base_page.py
from playwright.sync_api import Page, Locator
from typing import Union, List

class BasePage:
    def __init__(self, page: Page):
        self.page = page


    def _get_locator(self, selector: str, timeout: int = 10000) -> Locator:
        """
        统一获取 Locator, Playwright 会自动等待元素可见且可交互
        不再需要显示等待！
        """
        return self.page.locator(selector).first


    def click(self, selector: str):
        """封装点击，自动等待元素可点击"""
        self._get_locator(selector).click()


    def fill(self, selector: str, text: str):
        """封装输入，自动等待元素可输入"""
        self._get_locator(selector).fill(text)


    def get_text(self, selector: str) -> str:
        """获取文本，自动等待元素可见"""
        return self._get_locator(selector).text_content()


    def is_visible(self, selector: str) -> bool:
        """检查元素是否可见"""
        return self._get_locator(selector).is_visible()


    def select_option(self, selector: str, value: Union[str, List[str]]):
        """
        封装下拉框选择，支持单选和多选
        :param selector: 选择器
        :param value: 选项值（支持字符串或字符串列表）
        """
        self._get_locator(selector).select_option(value)


    def select_custom_option(self, trigger_selector: str, option_selector: str):
        """
        封装自定义下拉框选择（非原生 select 标签）
        :param trigger_selector: 触发下拉的按钮/输入框选择器
        :param option_selector: 目标选项的选择器
        """
        self.click(trigger_selector)
        self.click(option_selector)


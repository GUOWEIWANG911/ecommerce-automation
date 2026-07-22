import time
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.config import WAIT_TIMEOUT_NORMAL, WAIT_TIMEOUT_CRITICAL, WAIT_TIMEOUT_DYNAMIC
from utils.config import CHROME_DRIVER_PATH

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.default_wait = WebDriverWait(driver, WAIT_TIMEOUT_DYNAMIC) # 设置10秒显示等待

    def find_element(self, locator, timeout=None):
        """查找元素，带有显示等待"""
        wait = WebDriverWait(self.driver, timeout) if timeout else self.default_wait

        try:
            return wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            # 超时后自动截图，方便排查是网络慢还是元素变了
            self.save_screenshot("element_not_found")
            logger.error(f"元素未找到：{locator}，超时时间：{timeout or WAIT_TIMEOUT_DYNAMIC}秒")
            raise  # 重新抛出异常，让测试用例正常报错

    def save_screenshot(self, name="debug"):
        """保存截图到 debug_screenshots 文件夹"""
        import os
        dir_name = "debug_screenshots"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        timestamp = int(time.time())
        file_path = os.path.join(dir_name, f"{name}_{timestamp}.png")
        self.driver.save_screenshot(file_path)
        logger.info(f"截图已保存：{file_path}")

    def click(self, locator):
        """点击元素"""
        self.find_element(locator).click()

    def input_text(self, locator, text):
        """输入文本"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """获取元素文本"""
        return self.find_element(locator).text
    
import sys
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from utils.config import CHROME_DRIVER_PATH

# 将项目根目录添加到 Python 模块搜索路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# @pytest.fixture(scope="class")
# def driver():
#     # 1. 创建 Service 对象
#     service = Service(CHROME_DRIVER_PATH)
    
#     # 2. 使用 service 启动浏览器
#     driver = webdriver.Chrome(service=service)
    
#     # 3. 最大化窗口（可选）
#     driver.maximize_window()
    
#     # 4. 把 driver 提供给测试用例
#     yield driver
    
#     # 5. 测试结束后关闭浏览器
#     driver.quit()
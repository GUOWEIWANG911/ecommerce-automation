import os
import pytest
import yaml
from selenium import webdriver

def load_login_cases():
    """读取 YAML 测试数据"""
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data.yaml")
    with open(data_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data['login_cases']

@pytest.fixture(scope="session")
def global_test_data():
    """Session级别Fixture，供测试方法直接调用"""
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data.yaml")
    with open(data_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="function")
def driver():
    """初始化 Chrome 浏览器"""
    options = webdriver.ChromeOptions()
    # 移除所有防检测配置，让浏览器"坦诚"运行
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)    # 设置页面加载超时为 30 秒，给足加载时间
    driver.implicitly_wait(10)  # 隐式等待 10 秒
    
    yield driver
    
    # 清理：关闭浏览器
    driver.quit()
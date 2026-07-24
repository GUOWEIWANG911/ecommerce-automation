# utils/config.py
import os

BASE_URL = "https://petstore.octoperf.com"
USERNAME = "j2ee"
PASSWORD = "j2ee"
SEARCH_KEYWORD = "dog"

# ✅ 显式等待超时时间，方便不同环境调整
EXPLICIT_WAIT_TIMEOUT = 30

# ✅ 分级超时配置
WAIT_TIMEOUT_NORMAL = 10     # 普通元素（输入框、链接、按钮）
WAIT_TIMEOUT_CRITICAL = 15   # 核心业务元素（登录、下单、订单号）
WAIT_TIMEOUT_DYNAMIC = 20    # 动态加载内容（弹窗、AJAX结果）

# 拼接出正确的驱动路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME_DRIVER_PATH = os.path.join(PROJECT_ROOT, 'drivers', 'chromedriver.exe')
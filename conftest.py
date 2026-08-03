# conftest.py
import os
import pytest
import yaml
from playwright.sync_api import sync_playwright, Page


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


@pytest.fixture(scope="session")
def browser():
    """会话级浏览器实例，所有测试共享，避免重复启动"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        yield browser
        browser.close()


@pytest.fixture
def page(browser) -> Page:
    """
    函数级页面实例，每个测试用例独立
    自动设置视口、开启 Trace 录制、测试结束后自动清理
    """
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        # 可选：设置基础URL，page.goto() 时可使用相对路径
        # base_url="https://petstore.octoperf.com"
    )
    page = context.new_page()

    # 开启 Trace 录制（调试神器，失败时自动生成 trace.zip）
    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    yield page

    # 测试结束后保存 Trace 文件
    test_name = os.environ.get("PYTEST_CURRENT_TEST", "unknown").split("::")[-1]
    trace_path = f"traces/{test_name}.zip"
    os.makedirs("traces", exist_ok=True)
    context.tracing.stop(path=trace_path)

    context.close()
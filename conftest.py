# conftest.py
import os
import yaml
import pytest
import allure
from typing import Generator
from playwright.sync_api import sync_playwright, Page, Browser


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
        browser_type = os.environ.get("BROWSER_TYPE", "chromium")

        if browser_type == "firefox":
            browser = p.firefox.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
        elif browser_type == "webkit":
            browser = p.webkit.launch(
                headless=True,
                # args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
        else:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )

        yield browser
        browser.close()


@pytest.fixture
def page(browser) -> Generator[Page, None, None]:
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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    钩子函数：在测试用例执行完毕后调用
    ：param item: 测试用例对象
    ：param call: 调用对象，包含执行结果
    """
    # 执行下一个钩子或测试和用例
    outcome = yield
    # 获取测试结果
    rep = outcome.get_result()

    # 判断是否是“call”阶段（即测试用例主体执行阶段）且结果为失败
    if rep.when == "call" and rep.failed:
        # 尝试获取 page 对象
        page = item.funcargs.get("page")    # 通过 item.funcargs 获取 fixture 

        if page:
            try:
                # 截图并保存为字节流
                screenshot = page.screenshot()
                # 将截图附加到 Allure 报告
                allure.attach(
                    screenshot,
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                # 如果截图失败（比如页面已关闭），记录日志但不中断报告生成
                allure.attach(
                    f"截图失败：{str(e)}",
                    name="截图错误信息",
                    attachment_type=allure.attachment_type.TEXT
                )        

# 自定义钩子
def pytest_addhooks(pluginmanager):
    class MyCustomHooks:
        @pytest.hookspec(firstresult=True)
        def pytest_my_custom_greeting(self, name):
            """我的自定义问候钩子"""
            pass

    pluginmanager.add_hookspecs(MyCustomHooks)


@pytest.hookimpl
def pytest_my_custom_greeting(name):
    print(f"\n🎉 自定义钩子触发啦！你好，{name}！测试已经全部结束！")
    return "Greeting Success"


def pytest_sessionfinish(session, exitstatus):
    print("\n🚀 官方钩子：pytest_sessionfinish 正在执行...")
    
    # 调用我们自定义的钩子，并传入参数
    result = session.config.pluginmanager.hook.pytest_my_custom_greeting(name="测试工程师")
    print(f"📢 自定义钩子的返回值是：{result}")

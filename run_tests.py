# # run_tests.py
# import unittest
# import sys
# import os
# import time
# from html_testRunner import HTMLTestRunner

# # --- 1. 环境配置 ---
# # 将项目根目录添加到系统路径，确保能导入 pages 和 utils
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# # 2. 定义报告存放路径
# REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
# if not os.path.exists(REPORT_DIR):
#     os.makedirs(REPORT_DIR)

# # 3. 生成带时间戳的报告文件名
# timestamp = time.strftime("%Y%m%d_%H%M%S")
# report_path = os.path.join(REPORT_DIR, f"test_report_{timestamp}.html")

# # 4. 主程序入口
# if __name__ == '__main__':
#     # A. 加载测试用例
#     loader = unittest.TestLoader()
#     suite = loader.discover(
#         start_dir="tests",       # 测试用例所在目录
#         pattern="test_*.py"      # 匹配测试文件
#     )

#     # B. 执行测试并生成报告
#     with open(report_path, "wb") as f:
#         runner = HTMLTestRunner(
#             stream=f,
#             title="电商自动化测试报告",
#             description="包含登录、下单等核心业务流程",
#             tester="Acho"        # 测试人员姓名
#         )
#         runner.run(suite)

#     # C. 打印报告路径，方便快速打开
#     print(f"\n✅ 测试报告已生成: {report_path}")


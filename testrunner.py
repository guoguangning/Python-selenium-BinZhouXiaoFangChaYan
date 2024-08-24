import unittest
from HTMLTestRunner import HTMLTestRunner
import time
import os

# 获取当前时间，并定义报告的文件名和路径
now = time.strftime("%Y%m%d%H%M", time.localtime())
filename = now + "report.html"
report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_report')
report_path = os.path.join(report_dir, filename)

# 创建报告目录（如果不存在）
os.makedirs(report_dir, exist_ok=True)

# 定义测试套件的加载路径和模式
start_dir = './testsuites/unittest'
pattern = 'testLogin_un.py'

# 使用 unittest 的 discover 方法加载测试套件
testsuite = unittest.defaultTestLoader.discover(
    start_dir=start_dir,
    pattern=pattern,
    top_level_dir=None
)

try:
    with open(report_path, 'w', encoding='utf-8') as f:
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=f,
            verbosity=2,
            title='gateway UI report',
            description='执行情况'
        )
        runner.run(testsuite)
except Exception as e:
    print(f"An error occurred: {e}")

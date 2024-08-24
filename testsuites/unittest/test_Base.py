from selenium import webdriver
import unittest


class TestBase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  # 驱动浏览器
        self.driver.implicitly_wait(10)  # 设置隐式等待
        self.driver.maximize_window()  # 最大化浏览器

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
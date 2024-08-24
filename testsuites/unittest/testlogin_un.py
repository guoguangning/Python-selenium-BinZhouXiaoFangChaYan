import time
from testsuites.unittest.test_Base import TestBase
from page_objects.loginPage import LoginPage


class BaiduSearch(TestBase):

    def test_baidu_search(self):
        """
        这里一定要test开头，把测试逻辑代码封装到一个test开头的方法里。
        :return:
        """
        self.input = LoginPage(self.driver)
        self.input.goto_login_page()
        self.input.input_username('18812345678')  # 调用页面对象中的方法
        self.input.input_password('qpal20@24')
        self.input.submit_btn()  # 调用页面对象类中的点击搜索按钮方法
        time.sleep(2)
        title = self.input.get_title()
        try:
            assert title == '建设工程消防查验及审查验收备案申报服务系统'
            self.input.get_windows_img()  # 调用基类截图方法
            print('Test Pass.')
        except Exception as e:
            self.input.get_windows_img()  # 调用基类截图方法
            print('Test Fail.', format(e))

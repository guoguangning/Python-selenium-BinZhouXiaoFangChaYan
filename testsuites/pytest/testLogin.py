import time
import allure
import pytest
from selenium import webdriver
from framework.logger import Logger
from page_objects.loginPage import LoginPage

logger = Logger("testLogin").get_log()


@allure.description("登录")
class TestLogin(object):
    login_data = [
        ('18812345678', 'qpal20@24', 'https://xfcy.bzsczx.cn/taskList/untaskList')
    ]

    def setup_class(self) -> None:
        self.driver = webdriver.Chrome()
        self.LoginPage = LoginPage(self.driver)
        self.LoginPage.goto_login_page()

    def teardown_class(self) -> None:
        # self.driver.quit()
        self.LoginPage.quit_browser()

    @pytest.mark.parametrize('username, password, expected', login_data)
    def test_login(self, username, password, expected):
        self.LoginPage.input_username(username)  # 调用页面对象中输入的方法
        self.LoginPage.input_password(password)  # 调用页面对象中输入的方法
        self.LoginPage.submit_btn()  # 调用页面对象类中的点击登录按钮方法
        self.LoginPage.click_btn()  # 调用页面对象类中的点击btn按钮方法
        time.sleep(2)
        url = self.LoginPage.get_url()
        try:
            assert url == expected
            self.LoginPage.get_windows_img()  # 调用基类截图方法
            logger.info('Test Pass.')
        except AssertionError as e:
            self.LoginPage.get_windows_img()  # 调用基类截图方法
            logger.error('Test Fail. Assertion Error: {}'.format(e))
        except Exception as e:
            self.LoginPage.get_windows_img()  # 调用基类截图方法
            logger.error('Test Fail. Exception: {}'.format(e))


if __name__ == '__main__':
    pytest.main(['testLogin.py'])

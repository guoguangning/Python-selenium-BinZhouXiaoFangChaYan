from framework.base_Page import BasePage
from selenium.webdriver.common.by import By
from framework.logger import Logger

logger = Logger("login_page").get_log()


class LoginPage(BasePage):
    # 定位器
    username_input = (By.ID, 'username')
    password_input = (By.ID, 'password')
    search_submit = (By.ID, 'loginForm_su')
    btn_click = (By.ID, 'btn')  # 消防查验
    xf_click = (By.ID, 'xf')  # 消防

    def __init__(self, driver):
        super().__init__(driver)  # 使用super()调用父类构造函数

    def goto_login_page(self):
        """打开登录页面"""
        self.open()
        self.driver.implicitly_wait(10)  # 设置隐式等待
        self.driver.maximize_window()  # 最大化浏览器
        logger.info("Navigated to login page and maximized window")

    def input_username(self, text):
        """输入用户名"""
        try:
            self.find_element(self.username_input)
            self.send_keys(self.username_input, text)
            logger.info("Entered username: %s", text)
        except Exception as e:
            logger.error("Failed to enter username: %s", e)
            raise

    def input_password(self, text):
        """输入密码"""
        try:
            self.find_element(self.password_input)
            self.send_keys(self.password_input, text)
            logger.info("Entered password")
        except Exception as e:
            logger.error("Failed to enter password: %s", e)
            raise

    def submit_btn(self):
        """点击提交按钮"""
        try:
            self.find_element(self.search_submit)
            self.click(self.search_submit)
            logger.info("Clicked btn button")
            # self.sleep(2)
        except Exception as e:
            logger.error("Failed to click submit button: %s", e)
            raise

    def click_btn(self):
        """点击消防查验"""
        try:
            self.find_element(self.btn_click)
            self.click(self.btn_click)
            logger.info("Clicked btn button")
            # self.sleep(2)
        except Exception as e:
            logger.error("Failed to click btn button: %s", e)
            raise

    def click_xf(self):
        """点击消防"""
        try:
            self.find_element(self.xf_click)
            self.click(self.xf_click)
            logger.info("Clicked submit button")
            # self.sleep(2)
        except Exception as e:
            logger.error("Failed to click xf button: %s", e)
            raise

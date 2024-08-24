import configparser
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import os.path
from framework.logger import Logger
from selenium.webdriver.support import expected_conditions as EC

# 创建一个日志实例
logger = Logger("BasePage").get_log()


class BasePage(object):
    """
    定义一个页面基类，让所有页面都继承这个类，封装一些常用的页面操作方法
    """

    def __init__(self, driver, config_file_path='C:\case\BinZhouXiaoFangChaYan\config.ini'):
        self.driver = driver
        self.url = self.get_url_from_config(config_file_path)  # 读取 URL
        if self.url:
            print(f"URL retrieved from config: {self.url}")
        else:
            print("Failed to retrieve URL from config.")

    def open(self):
        """使用配置文件中的 URL 打开网页"""
        if self.url:
            self.driver.get(self.url)
            logger.info(f"Opened URL: {self.url}")
        else:
            logger.error("URL is not set. Cannot open page.")

    @classmethod
    def get_url_from_config(cls, config_file_path):
        """从配置文件中获取 URL"""
        config = configparser.ConfigParser()
        try:
            config.read(config_file_path, encoding='utf-8')
            # with open(config_file_path, 'r', encoding='utf-8') as file:
            #     config.read_file(file)
            # 确保配置文件的 section 和 key 存在
            if 'testServer' not in config:
                raise KeyError("Section 'testServer' is missing from the config file.")
            if 'url' not in config['testServer']:
                raise KeyError("Key 'url' is missing from the 'testServer' section.")

            url = config.get('testServer', 'url')
            logger.info(f"Retrieved URL from config: {url}")
            return url
        except (configparser.Error, KeyError) as e:
            logger.error(f"Configuration error: {e}")
        except Exception as e:
            logger.error(f"Failed to retrieve URL from config: {e}")
        return None

    def quit_browser(self):
        """退出浏览器并结束测试"""
        self.driver.quit()
        logger.info("Browser closed.")

    def forward(self):
        """浏览器前进操作"""
        self.driver.forward()
        logger.info("Navigated forward.")

    def back(self):
        """浏览器后退操作"""
        self.driver.back()
        logger.info("Navigated backward.")

    def get_windows_img(self):
        """
        把截图保存到我们项目根目录的一个文件夹 Screenshots 下
        """
        # 构建文件夹路径
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Screenshots')

        # 创建 Screenshots 文件夹如果它不存在
        os.makedirs(file_path, exist_ok=True)

        # 创建截图文件名
        screen_name = os.path.join(file_path, time.strftime('%Y%m%d%H%M%S') + '.png')

        try:
            # 截图并保存
            self.driver.get_screenshot_as_file(screen_name)
            logger.info(f"Screenshot taken and saved to folder: {file_path}")
        except (IOError, OSError) as e:
            logger.error(f"Failed to take screenshot! {e}")

        # 定位元素方法

    def wait(self, loc, seconds=10, condition=EC.presence_of_element_located):
        """
        显示等待元素的出现
        :param loc: 元素的定位方式和定位值，例如(By.ID, "element_id")
        :param seconds: 最大等待时间
        :param condition: 期望的条件，如 presence_of_element_located、visibility_of_element_located 等
        """
        try:
            WebDriverWait(self.driver, seconds).until(condition(loc))
            logger.info(f"Waited for {seconds} seconds for element located by {loc}.")
        except Exception as e:
            logger.error(f"Failed to wait for element {loc}: {e}")
            self.get_windows_img()
            raise

    def find_element(self, loc):
        """
        定位元素，并等待直到元素可见
        :param loc: 元素的定位方式和定位值，例如(By.ID, "element_id")
        :return: 元素对象
        """
        logger.info(f"Attempting to find element located by {loc}.")
        try:
            self.wait(loc, condition=EC.presence_of_element_located)
            element = self.driver.find_element(*loc)
            logger.info(f"Element located by {loc} found successfully.")
            return element
        except Exception as e:
            logger.error(f"Failed to find element located by {loc}: {e}")
            self.get_windows_img()
            raise

    def get_text(self, loc):
        """
            获取指定元素的文本
            :param loc: 元素定位方式（如：('id', 'element_id')）
            :return: 元素的文本
        """
        element = self.find_element(loc)
        return element.text

    def send_keys(self, selector, text):
        """输入文本"""
        el = self.find_element(selector)
        el.clear()
        try:
            el.send_keys(text)
            logger.info("Had type \' %s \' in inputBox" % text)
        except Exception as e:
            logger.error("Failed to select in input box with %s" % e)
            self.get_windows_img()

    def clear(self, selector):
        """清除文本框"""
        el = self.find_element(selector)
        try:
            el.clear()
            logger.info("Clear text in input box before typing.")
        except Exception as e:
            logger.error("Failed to clear in input box with %s" % e)
            self.get_windows_img()

    def click(self, selector):
        """点击元素"""
        el = self.find_element(selector)
        try:
            el.click()
            logger.info("The element \'%s\' was clicked." % el.text)
        except Exception as e:
            logger.error("Failed to click the element with %s" % e)

    def move_element(self, loc, sloc):
        """鼠标事件（左键点击）"""
        mouse = self.find_element(loc)
        try:
            ActionChains(self.driver).move_to_element(mouse).perform()
            self.click(sloc)
            pass
        except Exception as e:
            logger.error("Failed to click move_element with %s" % e)
            self.get_windows_img()

    def get_title(self):
        """获取页面标题"""
        return self.driver.title

    def get_url(self):
        """获取页面url"""
        return self.driver.current_url

    @staticmethod
    def sleep(seconds):
        """强制等待"""
        time.sleep(seconds)
        logger.info("Sleep for %d seconds" % seconds)

    def switch_to(self, loc):
        """
        切换到指定的 iframe 或窗口
        :param loc: 元素定位方式（如：('id', 'iframe_id')）或窗口句柄
        """
        element = self.find_element(loc)
        self.driver.switch_to.frame(element)  # 切换到指定的 iframe

    def switch_to_window(self, window_handle):
        """
        切换到指定的窗口
        :param window_handle: 窗口句柄
        """
        self.driver.switch_to.window(window_handle)

    def switch_to_default_content(self):
        """
        切换回到默认内容
        """
        self.driver.switch_to.default_content()

    def select_by_value(self, loc, value):
        """
        从下拉框中选择一个值
        :param loc: 下拉框元素的定位方式（如：('id', 'dropdown_id')）
        :param value: 要选择的值
        """
        try:
            # 定位下拉框元素
            element = self.find_element(loc)

            # 创建 Select 对象
            select = Select(element)

            # 选择指定的值
            select.select_by_value(value)

            logger.info(f"Selected value '{value}' from dropdown with locator {loc}.")
        except Exception as e:
            logger.error(f"Failed to select value '{value}' from dropdown with locator {loc}: {e}")
            self.get_windows_img()

    def upload_file(self, loc, file_path):
        """
        上传文件
        :param loc: 文件上传<input> 元素的定位方式（如：('id', 'upload_element_id')）
        :param file_path: 要上传的文件的绝对路径
        """
        element = self.find_element(loc)
        try:
            element.send_keys(file_path)
            logger.info(f"File uploaded successfully: {file_path}")
        except Exception as e:
            logger.error(f"Failed to upload file {file_path}: {e}")
            self.get_windows_img()

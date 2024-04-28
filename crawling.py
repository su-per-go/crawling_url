import csv
import os
import re
import time
import pickle
import datetime

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import seleniumwire.undetected_chromedriver as uc

DRIVER_PATH = "driver/msedgedriver.exe"


class SaveRead:
    @staticmethod
    def save_response(file, file_name):  # 响应信息保存
        with open(file_name, "wb") as f:
            pickle.dump(file, f)

    @staticmethod
    def read_response(file_name):  # 读取响应信息
        with open(file_name, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def read_screenshot(file_name):
        pass

    @staticmethod
    def save_content(file, file_name):  # 页面数据保存
        with open(file_name, "w", encoding="utf8") as f:
            f.write(file)

    @staticmethod
    def read_content(file_name):  # 页面数据保存
        with open(file_name, "r") as f:
            return f.read()


class WebPageAnalyzer:
    def __init__(self, driver_path):
        chrome_options = uc.ChromeOptions()
        self.driver_path = driver_path
        self.options = webdriver.EdgeOptions()
        self.options.use_chromium = True
        self.options.add_argument('headless')
        self.options.add_argument(
            "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.69")
        self.options.add_argument('--window-size=1920,1080')
        self.driver = None

    def _initialize_driver(self):
        return webdriver.Edge(
            service=Service(executable_path=self.driver_path),
            options=self.options
        )

    def analyze_page(self, url, root_path, num):

        rw = SaveRead()
        current_url = ""
        response_status = 600  # 说明运行出错
        login_url = None
        try:
            self.driver = self._initialize_driver()
            self.driver.get(url)
            current_url = self.driver.current_url
            response_status = self.driver.execute_script("return window.performance.getEntries()[0].responseStatus;")

            # 滚动前页面内容
            before_html_code = self.driver.page_source
            # 向下滑动前响应信息
            before_response = self.driver.requests
            # 模拟滚动页面
            self.simulate_sliding()
            # 滚动后页面内容
            after_html_code = self.driver.page_source
            links = self.driver.find_elements(by=By.TAG_NAME, value="a")
            pattern = r"(login|signin|signup)"
            try:
                for url in links:
                    href = url.get_attribute("href")
                    if re.search(pattern, href):
                        login_url = href
                        break
            except Exception as e:
                pass
            # 滑动后响应信息
            after_response = self.driver.requests

        except Exception as e:
            print(e)
            path = os.path.join(root_path, str(num) + "/")
            os.mkdir(path)
            with open(os.path.join(path, "error.txt"), "w") as f:
                f.write(str(e))
        else:
            path = os.path.join(root_path, f"{num}-{response_status}/")
            if not os.path.exists(path):
                os.mkdir(path)
            # 存储滚动前信息
            rw.save_content(before_html_code, os.path.join(path, "before_content.txt"))
            rw.save_response(before_response, os.path.join(path, "before_response.pickle"))
            # 存储网页截图
            s = self.driver.get_window_size()
            h = self.driver.execute_script("return document.body.scrollHeight;")
            self.driver.set_window_size(s["width"], h)
            try:
                self.driver.save_screenshot(os.path.join(path, 'screenshot.png'))
            except Exception as e:
                pass
            # 存储后滚动信息
            rw.save_content(after_html_code, os.path.join(path, "after_content.txt"))
            rw.save_response(after_response, os.path.join(path, "after_response.pickle"))
            self.driver.quit()  # 关闭浏览器
        return response_status, current_url, login_url

    def simulate_sliding(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollTop=0);")
        page_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_step = 100
        while True:
            if scroll_step >= page_height or scroll_step > 10000:
                break
            next_scroll_position = min(scroll_step, page_height)
            scroll_step += 100
            self.driver.execute_script(f"window.scrollTo(0, {next_scroll_position});")
            time.sleep(2)


def save_url_info(file_name, request_url, num, file_num, code, response_url, login=False):
    current_time = datetime.datetime.now()
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hour = current_time.hour
    minute = current_time.minute
    formatted_time = f"{year}-{month:02d}-{day:02d}-{hour:02d}:{minute:02d}"
    with open(file_name, "a", newline='') as f:
        new_row = [num, file_num, request_url, code, response_url, str(login), formatted_time]
        csv_writer = csv.writer(f)
        csv_writer.writerow(new_row)

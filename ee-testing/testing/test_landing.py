import time
# from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest


class TestHost:
    def test_homepage(self):

        options = Options()
        options.add_argument("--headless=new")
        print('test loaded!')
        driver = webdriver.Chrome(options=options)
        # try driver = webdriver.Chrome('./chromedriver') with the driver in the project folder if you cant set to path

        driver.get('http://server:80/')
        # try driver.get(self.live_server_url) if driver.get('http://127.0.0.1:8000/') does not work
        print(driver.title)
        assert "Hello, world!" in driver.title

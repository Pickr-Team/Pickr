import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class SeleniumTest:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def tearDown(self):
        self.driver.quit()

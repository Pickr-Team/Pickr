# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium_test import SeleniumTest


class TestChangePassword(SeleniumTest):
    """
    Test the change password feature

    1. Login
    2. Click on the username
    3. Click on the change password link
    4. Enter the old password
    5. Enter the new password
    6. Enter the confirm password
    7. Click on the submit button
    8. Login again using the new password
    """

    def test_changePassword(self):
        self.driver.find_element(By.LINK_TEXT, "Change Password↗").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "oldPwd").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "oldPwd").send_keys("123456")
        time.sleep(1)
        self.driver.find_element(By.ID, "password").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "password").send_keys("123456")
        time.sleep(1)
        self.driver.find_element(By.ID, "confirm").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "confirm").send_keys("123456")
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".submit-button").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "user_name").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "user_name").send_keys("joojo")
        time.sleep(1)
        self.driver.find_element(By.ID, "password").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "password").send_keys("123456")
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".submit-button").click()
        time.sleep(1)

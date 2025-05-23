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


class TestManagerViewStudentSelection(SeleniumTest):
    """
    This test method tests the manager's ability to view student selection

    1. The manager logs in
    2. The manager views the student selection
    3. The manager logs out
    """

    def test_managerViewStudentSelection(self):
        process_btn = self.driver.find_element(By.LINK_TEXT, "Process")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", process_btn)
        time.sleep(1)
        process_btn.click()
        time.sleep(1)
        self.driver.find_element(By.ID, "fail_students").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".close").click()
        time.sleep(1)
        refresh_btn = self.driver.find_element(By.LINK_TEXT, "Refresh")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", refresh_btn)
        time.sleep(1)
        refresh_btn.click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Student Topics").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Check").click()
        time.sleep(1)
        status_select = self.driver.find_element(By.ID, "status")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", status_select)
        time.sleep(1)
        status_select.click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//option[. = 'Passed Verify']").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".submit-button").click()
        time.sleep(1)

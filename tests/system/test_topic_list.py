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


class TestTopicList(SeleniumTest):
    """
    This test method tests the user's ability to browse topics, filter or search for topics

    1. Open the website
    2. Browses topics, filters or searches for topics
    """

    def test_topic_list(self):
        self.driver.get("http://127.0.0.1:8000?test_name=view_topics")
        self.driver.maximize_window()
        self.driver.find_element(By.XPATH, "//em[contains(.,\'Topic List↗\')]").click()
        # type
        self.driver.find_element(By.CSS_SELECTOR, "#type-filter a:first-child").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, "#type-filter a:first-child").click()
        time.sleep(1)
        # supervisor
        self.driver.find_element(By.CSS_SELECTOR, "#supervisor-filter a:first-child").click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, "#supervisor-filter a:first-child").click()
        time.sleep(1)
        # search
        self.driver.find_element(By.ID, "name").send_keys('clivia')
        time.sleep(1)

        # self.driver.find_element(By.LINK_TEXT, "first_name0 last_name0").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name0 last_name0").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name1 last_name1").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name1 last_name1").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name1 last_name1").click()
        # element = self.driver.find_element(By.LINK_TEXT, "first_name1 last_name1")
        # actions = ActionChains(self.driver)
        # actions.double_click(element).perform()
        # self.driver.find_element(By.LINK_TEXT, "first_name4 last_name4").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name4 last_name4").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name1 last_name1").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name5 last_name5").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name9 last_name9").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name10 last_name10").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name10 last_name10").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name9 last_name9").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name5 last_name5").click()
        # self.driver.find_element(By.ID, "name").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name9 last_name9").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name9 last_name9").click()
        # element = self.driver.find_element(By.LINK_TEXT, "first_name9 last_name9")
        # actions = ActionChains(self.driver)
        # actions.double_click(element).perform()
        # self.driver.find_element(By.LINK_TEXT, "first_name10 last_name10").click()
        # self.driver.find_element(By.ID, "5").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name5 last_name5").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name1 last_name1").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name0 last_name0").click()
        # self.driver.find_element(By.ID, "4").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name10 last_name10").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name5 last_name5").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name0 last_name0").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name1 last_name1").click()
        # self.driver.find_element(By.ID, "4").click()
        # self.driver.find_element(By.CSS_SELECTOR, ".cell-4 > .w-layout-hflex").click()
        # self.driver.find_element(By.ID, "5").click()
        # self.driver.find_element(By.ID, "2").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name4 last_name4").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name4 last_name4").click()
        # self.driver.find_element(By.CSS_SELECTOR, ".cell-4 > .w-layout-hflex").click()
        # self.driver.find_element(By.CSS_SELECTOR, ".cell-4 > .w-layout-hflex").click()
        # self.driver.find_element(By.LINK_TEXT, "first_name6 last_name6").click()
        # self.driver.find_element(By.ID, "2").click()
        # self.driver.find_element(By.CSS_SELECTOR, ".link-block:nth-child(1)").click()
        # self.driver.back()
        # self.driver.find_element(By.CSS_SELECTOR, ".link-block:nth-child(2)").click()
        self.driver.quit()

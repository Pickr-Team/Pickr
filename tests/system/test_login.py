import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_test import SeleniumTest


# Remove inheritance from SeleniumTest when running this file stand-alone
class TestLogin(SeleniumTest):
    """
    Test three different users' login and logout

    1. Open the browser
    2. Visit the website
    3. Click the link "My Pickr"
    4. Enter the username and password
    5. Click the submit button
    6. Check the page content
    7. Click the logout link
    """
    def test_login(self):
        self.driver.get("http://127.0.0.1:8000?test_name=login")
        time.sleep(2)
        self.driver.set_window_size(1800, 1043)

        self.driver.find_element(By.LINK_TEXT, "My Pickr↗").click()
        self.driver.find_element(By.ID, "user_name").send_keys("202118020103")
        self.driver.find_element(By.ID, "password").send_keys("123456")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-button").click()
        time.sleep(2)
        assert self.driver.find_element(By.XPATH,
                                        "//p").text == "In this page,you can full the application form and check your topic apply result."
        self.driver.find_element(By.XPATH, "//em[contains(.,\'Logout↗\')]").click()

        self.driver.find_element(By.LINK_TEXT, "My Pickr↗").click()
        self.driver.find_element(By.ID, "user_name").send_keys("clivia")
        self.driver.find_element(By.ID, "password").send_keys("123456")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-button").click()
        time.sleep(2)
        assert self.driver.find_element(By.XPATH,
                                        "//p").text == "In this page,you can create your topic and check your applications."
        self.driver.find_element(By.XPATH, "//em[contains(.,\'Logout↗\')]").click()

        self.driver.find_element(By.LINK_TEXT, "My Pickr↗").click()
        self.driver.find_element(By.ID, "user_name").send_keys("Joojo")
        self.driver.find_element(By.ID, "password").send_keys("123456")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-button").click()
        time.sleep(1)

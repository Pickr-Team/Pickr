import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


class SeleniumTest:
    def __init__(self):
        # todo: why doesn't relative path work here?
        # chrome v131.xxx
        self.absolute_path = 'C:/Users/20854/Desktop/Pickr/tests/system/chromedriver-win64/chromedriver.exe'
        self.service = Service(executable_path=self.absolute_path)
        self.driver = None
        self.vars = {}

    def setUp(self):
        self.driver = webdriver.Chrome(service=self.service)

    def login(self, username):
        self.driver.get("http://127.0.0.1:8000")
        self.driver.maximize_window()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "My Pickr↗").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "user_name").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "user_name").send_keys(username)
        time.sleep(1)
        self.driver.find_element(By.ID, "password").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "password").send_keys("123456")
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".submit-button").click()
        time.sleep(1)

    def managerLogin(self):
        self.login('joojo')

    def supervisorLogin(self):
        self.login('clivia')

    def studentLogin(self):
        self.login('student_test_01')

    def tearDown(self):
        # logout
        self.driver.execute_script("window.scrollTo(0,0)")
        self.driver.find_element(By.LINK_TEXT, "My Pickr↗").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//em[contains(.,\'Logout↗\')]").click()
        self.driver.quit()

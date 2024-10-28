import unittest

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException

class TestFrontend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # initialize webdriver for webpage testing
        service = Service()
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=service, options=options)

    def test_home_page(self):
        # navigate to the homepage
        self.driver.get("http://host.docker.internal")

        # check that title is correct
        self.assertEqual("Scalable Homepage", self.driver.title, "Homepage title not displayed as \"Scalable Homepage\"")

    def test_professor_page(self):
        # navigate to specific professor page
        self.driver.get("http://host.docker.internal/professor/gerosa-marco")

        # wait up to 10 seconds for page to loading
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "professor-header")))

        # check that the professors name is being displayed correctly
        header_element = self.driver.find_element(By.CLASS_NAME, "professor-header")
        name = header_element.find_element(By.TAG_NAME, "h1")
        self.assertEqual("Gerosa,Marco Aurelio", name.text, "Professor page not displaying expected name")
        
        # navigate back to homepage
        self.driver.get("http://host.docker.internal")

# helper functions =========================
    def __retry_click(self, by, value, retries=3):
        # loop over number of retries specified (3 is usually enough)
        for _ in range(retries):
            # try to open profile
            try:
                btn = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((by, value)))
                btn.click()
                # exit upon success
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                # retry if exception thrown
                pass
        # throw exception if not found of stale state
        raise Exception(f"Element not found or still in stale state after {retries} retries, check to see if database has been deleted")

    def test_user_registration(self):
        # navigate to the homepage
        self.driver.get("http://host.docker.internal")

        # open general login form
        profile_pic_btn = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "popup-form")))
        profile_pic_btn.click()

        # open registration form
        register_form_btn = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "new-account")))
        register_form_btn.click()

        # get first name, last name, email, username, and password fields
        first_name_field = self.driver.find_element(By.CLASS_NAME, "first-name-field")
        last_name_field = self.driver.find_element(By.CLASS_NAME, "last-name-field")
        email_field = self.driver.find_element(By.CLASS_NAME, "email-field")
        username_field = self.driver.find_element(By.CLASS_NAME, "username-field")
        password_field = self.driver.find_element(By.CLASS_NAME, "password-field")

        # sign up with demo user
        first_name_field.send_keys("John")
        last_name_field.send_keys("Smith")
        email_field.send_keys("johnsmith123456@gmail.com")
        username_field.send_keys("johnsmith")
        password_field.send_keys("sjc623&$!jmaa*")

        # submit the new user form
        sign_up_btn = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "sign-up-btn")))
        sign_up_btn.click()

        # try to click button multiple times, otherwise exception raised
        self.__retry_click(By.CLASS_NAME, "popup-form")

        # wait for header to show and grab username
        username_element = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "h2.username")))

        # username will have @ symbol for tagging
        self.assertEqual("@johnsmith", username_element.text, "New user has not been registered")

    def test_user_login(self):
        # navigate to the homepage
        self.driver.get("http://host.docker.internal")

        # open general login form
        profile_pic_btn = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "popup-form")))
        profile_pic_btn.click()

        # press the sign out button (since user should already be logged in)
        # technically testing sign out functionality here too
        sign_out_btn = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "sign-out")))
        sign_out_btn.click()

        self.__retry_click(By.CLASS_NAME, "sign-out")

        # try to click button multiple times, otherwise exception raised
        self.__retry_click(By.CLASS_NAME, "popup-form")

        # get username and password fields
        username_field = self.driver.find_element(By.CLASS_NAME, "username-field")
        password_field = self.driver.find_element(By.CLASS_NAME, "password-field")

        # log in with demo user
        username_field.send_keys("johnsmith")
        password_field.send_keys("sjc623&$!jmaa*")

        # log the new user in
        login_btn = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "login-btn")))
        login_btn.click()

        # try to click button multiple times, otherwise exception raised
        self.__retry_click(By.CLASS_NAME, "popup-form")

        # wait for header to show and grab username
        username_element = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "h2.username")))

        # username will have @ symbol for tagging
        self.assertEqual("@johnsmith", username_element.text, "User has not been logged in")
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestFrontend("test_home_page"))
    suite.addTest(TestFrontend("test_professor_page"))
    suite.addTest(TestFrontend("test_user_registration"))
    suite.addTest(TestFrontend("test_user_login"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
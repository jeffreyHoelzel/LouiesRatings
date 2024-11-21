import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException

class TestUsingLocal(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    cls.driver = webdriver.Chrome(service=service, options=options)
    cls.driver.implicitly_wait(10)

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
    self.driver.get("http://localhost/")

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

    profile_pic_btn = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "popup-form")))

    try:
      # check if user already exists with that username/email
      user_exists = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "status-message")))

      # assert user is already in database using status message
      self.assertEqual("Username or email already in use.", user_exists.text, "Something went wrong fetching span element")

    except TimeoutException:
      # wait for header to show and grab username
      username_element = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "h2.username")))

      # username will have @ symbol for tagging
      self.assertEqual("@johnsmith", username_element.text, "New user has not been registered")

  def test_user_login(self):
    # navigate to the homepage
    self.driver.get("http://localhost/")

    # open general login form
    profile_pic_btn = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "popup-form")))
    profile_pic_btn.click()

    # try to sign in with new account, otherwise, try signing out first since registration test was just ran
    try:
      # get username and password fields
      username_field = self.driver.find_element(By.CLASS_NAME, "username-field")
      password_field = self.driver.find_element(By.CLASS_NAME, "password-field")

      # log in with demo user
      username_field.send_keys("johnsmith")
      password_field.send_keys("sjc623&$!jmaa*")
    except TimeoutException:
      # press the sign out button (since user should already be logged in)
      sign_out_btn = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "sign-out")))
      sign_out_btn.click()

      # open general login form
      profile_pic_btn = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "popup-form")))
      profile_pic_btn.click()

      # get username and password fields
      username_field = self.driver.find_element(By.CLASS_NAME, "username-field")
      password_field = self.driver.find_element(By.CLASS_NAME, "password-field")

      # log in with demo user
      username_field.send_keys("johnsmith")
      password_field.send_keys("sjc623&$!jmaa*")

    # log the new user in
    login_btn = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "login-btn")))
    login_btn.click()

    # wait for refresh
    time.sleep(5)

    # open general login form
    profile_pic_btn = WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "popup-form")))
    profile_pic_btn.click()

    # wait for header to show and grab username
    username_element = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "h2.username")))

    # username will have @ symbol for tagging
    self.assertEqual("@johnsmith", username_element.text, "User has not been logged in")

  @classmethod
  def tearDownClass(cls):
    cls.driver.quit()

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestUsingLocal("test_user_registration"))
    suite.addTest(TestUsingLocal("test_user_login"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
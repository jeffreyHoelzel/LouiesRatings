import unittest
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

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
        self.assertEqual("Louie's Ratings", self.driver.title, "Homepage title not displayed as \"Louie's Ratings\"")

    def test_professor_page(self):
        # navigate to specific professor page
        self.driver.get("http://host.docker.internal/professor/gerosa-marco")

        # wait up to 10 seconds for page to loading
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "professor-header")))

        # check that the professors name is being displayed correctly
        header_element = self.driver.find_element(By.CLASS_NAME, "professor-header")
        h1_elements = header_element.find_elements(By.TAG_NAME, "h1")
        h1_texts = [element.text for element in h1_elements]
        name = ','.join(h1_texts)    
        self.assertEqual("Gerosa,Marco Aurelio", name, "Professor page not displaying expected professor name in title")
        
        # navigate back to homepage
        self.driver.get("http://host.docker.internal")

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
        self.driver.get("http://host.docker.internal")

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

    def test_search(self):
        # navigate to the homepage
        self.driver.get("http://host.docker.internal")

        # search for a professor
        search_input = self.driver.find_element(By.CLASS_NAME, "search-bar")
        search_input.send_keys("gerosa")

        # wait up to 10 seconds for page to loading
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "dropdown")))

        # check that the professors name exists
        header_element = self.driver.find_element(By.CLASS_NAME, "dropdown")
        name = header_element.find_element(By.TAG_NAME, "li")
        self.assertEqual("Gerosa,Marco Aurelio", name.text, "Search page not displaying expected name")

        # click on the list item containing the name
        name.click()

        # wait for the new page to load (the professor page)
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "professor-header")))

        # verify the URL has the expected path
        current_url = self.driver.current_url
        self.assertIn("professor/gerosa-marco", current_url, "Routing did not work as expected")

        # navigate back to homepage
        self.driver.get("http://host.docker.internal")

        # get search input again
        search_input = self.driver.find_element(By.CLASS_NAME, "search-bar")

        # make a new search
        search_input.send_keys("cs386")

        # force wait two second
        self.driver.implicitly_wait(2)

        # wait up to 10 seconds for page to loading
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "dropdown")))

        # check that the class name exists
        header_element = self.driver.find_element(By.CLASS_NAME, "dropdown")
        name = header_element.find_element(By.TAG_NAME, "li")
        self.assertEqual("CS 386", name.text, "Search page not displaying expected name")

        # click on the list item containing the name
        name.click()

        # wait for the new page to load (the class page)
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "course-header")))

        # verify the URL has the expected path
        current_url = self.driver.current_url
        self.assertIn("class/CS-386", current_url, "Routing did not work as expected")

        

    def test_comments(self):
        # navigate to specific professor page
        self.driver.get("http://host.docker.internal")

        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "comments")))

        # get latest userId
        comment_list = self.driver.find_element(By.ID, "comment-list")
        comments = comment_list.find_elements(By.TAG_NAME, "li")

        user_id = 0

        if len(comments):
            latest_comment = comments[-1]
            user_id = latest_comment.get_attribute("id")
            user_id = int(user_id) + 1

        # find user input fields
        user_input = self.driver.find_element(By.ID, "userId")
        user_input.send_keys(f"{user_id}")

        # find comment input fields
        comment_input = self.driver.find_element(By.ID, "content")
        comment_input.send_keys("This is a test comment")

        # hit submit button
        submit_button = self.driver.find_element(By.ID, "submit")
        submit_button.click()

        # wait until comment is added
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.ID, f"{user_id}")))

        # check that the comment was added
        latest_comment = self.driver.find_element(By.ID, f"{user_id}")

        self.assertTrue(user_id == int(latest_comment.get_attribute("id")), f"Comment was not added {user_id} != {latest_comment.get_attribute('id')}")

        # delete the comment
        delete_button = latest_comment.find_element(By.CLASS_NAME, "trash-can")
        delete_button.click()

        # wait until comment is deleted
        WebDriverWait(self.driver, 10).until(expected_conditions.staleness_of(latest_comment))

        # check that the comment was deleted    
        comments = comment_list.find_elements(By.TAG_NAME, "li")
        latest_comment = comments[-1]

        self.assertTrue(user_id != int(latest_comment.get_attribute("id")), f"Comment was not deleted {user_id} == {latest_comment.get_attribute('id')}")
    
    def test_class_page(self):
        # navigate to specific professor page
        self.driver.get("http://host.docker.internal/class/cs-386")

        # wait up to 10 seconds for page to loading
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "course-header")))

        # check that the professors name is being displayed correctly
        header_element = self.driver.find_element(By.CLASS_NAME, "course-header")
        name = header_element.find_element(By.TAG_NAME, "h1")
        self.assertEqual("CS 386", name.text, "Class page not displaying expected class name in title")

    def test_charts(self):
        # test that charts were found for a specific professor page and class page
        for i in range(2):
            if i == 0:
                # navigate to specific professor page
                self.driver.get("http://host.docker.internal/professor/gerosa-marco")
                testing_page = "professor"
            else:
                # navigate to specific professor page
                self.driver.get("http://host.docker.internal/class/cs-386")
                testing_page = "class"

            # wait up to 10 seconds for page to loading
            WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_all_elements_located((By.CSS_SELECTOR, ".recharts-cartesian-axis-tick-value")))

            # check that the professors name is being displayed correctly
            all_axis_labels = self.driver.find_elements(By.CSS_SELECTOR, ".recharts-cartesian-axis-tick-value")
            x_axis_labels = [label.text for label in all_axis_labels[0:7]]
            self.assertEqual(['A', 'B', 'C', 'D', 'F', 'P', 'W'], x_axis_labels, f"Chart on {testing_page} page not displaying correctly")

    def test_ratings(self):
        # test that average rating and rating submit were found for a specific professor page and class page
        for i in range(2):
            if i == 0:
                # navigate to specific professor page
                self.driver.get("http://host.docker.internal/professor/gerosa-marco")
                testing_page = "professor"
            else:
                # navigate to specific professor page
                self.driver.get("http://host.docker.internal/class/cs-386")
                testing_page = "class"

            # wait up to 10 seconds for page to loading
            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "star-ratings")))

            # check that the both average ratings and ratings submit are being displayed correctly
            ratings = self.driver.find_elements(By.CLASS_NAME, "star-ratings")
            self.assertEqual(2, len(ratings), f"Chart on {testing_page} page not displaying correctly")
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestFrontend("test_home_page"))
    suite.addTest(TestFrontend("test_professor_page"))
    suite.addTest(TestFrontend("test_class_page"))
    suite.addTest(TestFrontend("test_user_registration"))
    suite.addTest(TestFrontend("test_user_login"))
    suite.addTest(TestFrontend("test_search"))
    suite.addTest(TestFrontend("test_charts"))
    suite.addTest(TestFrontend("test_ratings"))

    runner = unittest.TextTestRunner()
    runner.run(suite)

import unittest

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

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

    def test_search(self):
        # navigate to the homepage
        self.driver.get("http://host.docker.internal")

        # search for a professor
        search_input = self.driver.find_element(By.CLASS_NAME, "search-bar")
        search_input.send_keys("gerosa")
        search_input.submit()

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
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
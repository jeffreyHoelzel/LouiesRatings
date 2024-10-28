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
        self.assertEqual("Gerosa,Marco Aurelio", name.text, "Professor page not displaying expected professor name in title")
        
        # navigate back to homepage
        self.driver.get("http://host.docker.internal")
    
    def test_class_page(self):
        # navigate to specific professor page
        self.driver.get("http://host.docker.internal/class/cs-386")

        # wait up to 10 seconds for page to loading
        WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "class-header")))

        # check that the professors name is being displayed correctly
        header_element = self.driver.find_element(By.CLASS_NAME, "class-header")
        name = header_element.find_element(By.TAG_NAME, "h1")
        self.assertEqual("CS 386", name.text, "Class page not displaying expected class name in title")
        
        # navigate back to homepage
        self.driver.get("http://host.docker.internal") 

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
            WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, ".recharts-cartesian-axis-tick-value")))

            # check that the professors name is being displayed correctly
            all_axis_labels = self.driver.find_elements(By.CSS_SELECTOR, ".recharts-cartesian-axis-tick-value")
            x_axis_labels = [label.text for label in all_axis_labels[0:7]]
            self.assertEqual(['A', 'B', 'C', 'D', 'F', 'P', 'W'], x_axis_labels, f"Chart on {testing_page} page not displaying correctly")
        
        # navigate back to homepage
        self.driver.get("http://host.docker.internal")
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
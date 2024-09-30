from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import pandas as pd

NAU_CLASS_DISTRIBUTION_URL = "https://www7.nau.edu/pair/reports/ClassDistribution"

term = "Spring 2024"
subject = "CS"

service = Service(executable_path="chromedriver.exe")
options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(service=service, options=options)

driver.get(NAU_CLASS_DISTRIBUTION_URL)

# select term by name
input_element = Select(driver.find_element(By.NAME, "ctl00$MainContent$TermList"))
input_element.select_by_visible_text(term)

# select subject by name
input_element = Select(driver.find_element(By.NAME, "ctl00$MainContent$SubjectList"))
input_element.select_by_visible_text(subject)

# click submit
driver.find_element(By.ID, "MainContent_Button1").click()

# wait until the first table is done loading (max 10 seconds)
WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "MainContent_GridView1")))

# get the html from curent page
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

# extract the table
table = soup.find("table", id="MainContent_GridView1").find("tbody")

if table:
    class_distr_data = list()

    # loop through each row in the table
    for row_idx, tr in enumerate(table.find_all("tr")):
        row_data = [td.text for td in tr.find_all("td")]

         # skip any rows that are blank
        if row_data:
            # assume first row is the header
            if row_idx == 0:
                col_headers = row_data
            # otherwise add row to table
            else:
                class_distr_data.append(row_data)
    
    # create data frame
    class_distr_table = pd.DataFrame(class_distr_data, columns=col_headers)

    print(class_distr_table)
else:
    print("Table not found.")

driver.quit()

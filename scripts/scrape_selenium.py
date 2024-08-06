NUM_PAGES = 2

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import requests
from urllib.parse import urlsplit
import os

links = []

# Open browser
driver = webdriver.Chrome()

for page_num in range(1,NUM_PAGES+1):
    driver.get("https://www.loc.gov/search/?fa=original-format:periodical&q=%22employment+discrimination%22&sp="+str(page_num))

    # Locate all parent elements (e.g., with class name 'parent-class')
    parent_elements = driver.find_elements(By.CLASS_NAME, 'item-description-title')
    
    # Iterate over each parent element
    for parent_element in parent_elements:
        # Find all child elements with the tag 'a' within the parent element
        child_elements = parent_element.find_elements(By.TAG_NAME, 'a')
        
        # Iterate over the child elements and get their href attribute values
        href_values = [element.get_attribute('href') for element in child_elements]
         
        for link in href_values:
            links.append(link)
            print("Appended" + link)

# Close browser
driver.quit()

driver = webdriver.Chrome()

# Iterate over each pdf's link
for link in links:
    driver.get(link)

    select_element = Select(driver.find_element(By.ID, 'select-resource0'))
    first_option = select_element.options[0]
    first_option_value = first_option.get_attribute("value")
    print("Read file" + first_option_value)

    # Extract filename from the URL
    path = urlsplit(first_option_value).path
    filename = os.path.basename(path)
    
    # Download the PDF
    response = requests.get(first_option_value)
    
    # Save the PDF to a file
    with open("data/" + filename, 'wb') as file:
        file.write(response.content)
    
    print(f'\nDownloaded file saved as: {filename}')

driver.quit()

print("\n\nEnd")


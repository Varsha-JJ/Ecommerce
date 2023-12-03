import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains

service = Service(executable_path=r"C:\documents\Store\firststep\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("http://127.0.0.1:8000/login/")

# Locate the username and password fields and input the credentials
username_field = driver.find_element(By.NAME, "email")
username_field.send_keys("onlinefirststep1@gmail.com")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("Firststep@123")

# Submit the login form
password_field.send_keys(Keys.RETURN)

driver.get("http://127.0.0.1:8000/admin_subaddcategory/")

# Locate the username and password fields and input the credentials


category_field = driver.find_element(By.NAME, "cate_name")
category_field .send_keys("Skirts")

productname_field = driver.find_element(By.NAME, "category")
productname_field .send_keys("GIRLS")



button = driver.find_element(By.ID, "sbtn")
if button.is_displayed():
    button.click()
else:
    # If the button is not visible, you can try scrolling down to it or using ActionChains to move to it
    actions = ActionChains(driver)
    actions.move_to_element(button).click().perform()


driver.get("http://127.0.0.1:8000/admin_subaddcategory/")


# Wait for the page to load and check for the presence of the dashboard element
dashboard_element = driver.find_element(By.XPATH, "//strong[contains(text(), 'Add sub-category')]")
if dashboard_element:
    print("Test Passed")
else:
    print("Test failed.")
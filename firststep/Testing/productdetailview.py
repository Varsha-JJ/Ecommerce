import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By

service = Service(executable_path=r"C:\documents\Store\firststep\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("http://127.0.0.1:8000/login/")

# Locate the username and password fields and input the credentials
username_field = driver.find_element(By.NAME, "email")
username_field.send_keys("sreelekshmianil90@gmail.com")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("Varu@123")

# Submit the login form
password_field.send_keys(Keys.RETURN)

# Wait for the page to load and check for the presence of the dashboard element
dashboard_element = driver.find_element(By.XPATH, "//a[contains(text(), 'My profile')]")

driver.get("http://127.0.0.1:8000/shop/")

driver.get("http://127.0.0.1:8000/product_detail/27/")


product_addcart = driver.find_element(By.XPATH, "//p[contains(text(), 'PRODUCT DESCRIPTION')]")

if product_addcart:
    print("Test Passed")
else:
    print("Test Failed")



# Close the browser
driver.quit()
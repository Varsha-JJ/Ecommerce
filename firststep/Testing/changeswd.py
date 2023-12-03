import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
service = Service(executable_path=r"C:\documents\Store\firststep\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("http://127.0.0.1:8000/login/")

# Locate the username and password fields and input the credentials
username_field = driver.find_element(By.NAME, "email")
username_field.send_keys("sreelekshmianil90@gmail.com")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("Varu@1234")
password_field.send_keys(Keys.RETURN)


driver.get("http://127.0.0.1:8000/changepassword/")

oldpass_field = driver.find_element(By.NAME, "current_password")
oldpass_field.send_keys(str("Varu@1234"))

newpass_field = driver.find_element(By.NAME, "new_password")
newpass_field.send_keys(str("Varu@123"))


conpass_field = driver.find_element(By.NAME, "confirm_password")
conpass_field.send_keys(str("Varu@123"))
conpass_field.send_keys(Keys.RETURN)


driver.get("http://127.0.0.1:8000/login/")
username_field = driver.find_element(By.NAME, "email")
username_field.send_keys("sreelekshmianil90@gmail.com")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("Varu@123")
password_field.send_keys(Keys.RETURN)


dashboard_element = driver.find_element(By.XPATH, "//a[contains(text(), 'My profile')]")
if dashboard_element:
    print("Test Passed")
else:
    print("Test Failed")

driver.quit()
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
password_field.send_keys("Varu@123")
password_field.send_keys(Keys.RETURN)


# Wait for the page to load and check for the presence of the dashboard element
dashboard_element = driver.find_element(By.XPATH, "//a[contains(text(), 'My profile')]")

driver.get("http://127.0.0.1:8000/account/")

# dashboard_element = driver.find_element(By.XPATH, "//a[contains(text(), 'Account details')]")

firstname_field = driver.find_element(By.NAME, "fname")
firstname_field.send_keys(str("Sreelekshmi"))

lastname_field = driver.find_element(By.NAME, "lname")
lastname_field.send_keys(str("Anilkumar"))

address_field = driver.find_element(By.NAME, "addres")
address_field.send_keys(str("kunnathettu"))



phone_field = driver.find_element(By.NAME, "phone")
phone_field.send_keys(str("994534567"))

city_field = driver.find_element(By.NAME, "city")
city_field.send_keys(str("Kovapally"))

state_field = driver.find_element(By.NAME, "district")
state_field.send_keys(str("Kerala"))

pincode_field = driver.find_element(By.NAME, "pincode")
pincode_field.send_keys(str("673592"))

pincode_field.send_keys(Keys.RETURN)
time.sleep(5)
dashboard_element = driver.find_element(By.XPATH, "//a[contains(text(), 'Dashboard')]")
if dashboard_element:
    print("Test Passed")
else:
    print("Test Failed")

driver.quit()



























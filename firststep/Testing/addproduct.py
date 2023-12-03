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
username_field.send_keys("varshajj2000@gmail.com")

password_field = driver.find_element(By.NAME, "password")
password_field.send_keys("Varu@123")

# Submit the login form
password_field.send_keys(Keys.RETURN)

driver.get("http://127.0.0.1:8000/product/")

# Locate the username and password fields and input the credentials
productname_field = driver.find_element(By.NAME, "category")
productname_field .send_keys("Shirt")

category_field = driver.find_element(By.NAME, "pname")
category_field .send_keys("Striped T-Shirt Giraffe Print - Red")

productname_field = driver.find_element(By.NAME, "pname")
productname_field .send_keys("Striped T-Shirt Giraffe Print - Red")

desc_field = driver.find_element(By.NAME, "pdesc")
desc_field.send_keys("Fabric- Cotton Jersey/Knit, Sleeves - Half Sleeves, Neck - Henley Neck ,Pattern - Stripes & Giraffe Print, Occasion - Casual Wear")

productimage_field = driver.find_element(By.NAME, "pimg")
productimage_field.send_keys(r"C:\documents\Store\firststep\product_image\shirtss.jpg")

price_field = driver.find_element(By.NAME, "price")
price_field.send_keys("500")

stock_field = driver.find_element(By.NAME, "stock")
stock_field.send_keys("7")

button = driver.find_element(By.ID, "my-btn")
if button.is_displayed():
    button.click()
else:
    # If the button is not visible, you can try scrolling down to it or using ActionChains to move to it
    actions = ActionChains(driver)
    actions.move_to_element(button).click().perform()


# time.sleep(2)
driver.get("http://127.0.0.1:8000/product/")
# time.sleep(5)

# Wait for the page to load and check for the presence of the dashboard element
dashboard_element = driver.find_element(By.XPATH, "//h3[contains(text(), 'PRODUCT')]")
if dashboard_element:
    print("Test Passed")
else:
    print("Test failed.")
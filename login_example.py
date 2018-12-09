from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "https://example.com/login/"
user = "username"
password = "password"

driver = webdriver.Chrome()
driver.implicitly_wait(3)

driver.get(url)

elem = driver.find_element_by_id("login_id")
elem.clear()
elem.send_keys(user)

elem = driver.find_element_by_id("login_password")
elem.clear()
elem.send_keys(password)

elem = driver.find_element_by_id("login_button")
elem.click()

import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
# driver.implicitly_wait(0)
driver.maximize_window()
driver.get("http://enroll-me.iiet.pl/")
time.sleep(2)
content = driver.find_element_by_xpath(
    '/html/body/div[2]/div[2]/form/div[4]/div/div/button[2]')
print(content)
content.click()

login = driver.find_element_by_xpath('//*[@id="student_username"]')
password = driver.find_element_by_xpath('//*[@id="student_password"]')
login.send_keys("")
password.send_keys("")
login_button = driver.find_element_by_xpath(
    '/html/body/div/div[2]/div/form/div[2]/input')
login_button.click()


enrollment_button = driver.find_element_by_xpath(
    '/html/body/div[1]/div/div[2]/div[2]/a')
enrollment_button.click()

all_plans = driver.find_element_by_xpath(
    '//*[@id="mainForm:j_id_x:tbody_element"]')
print(all_plans)

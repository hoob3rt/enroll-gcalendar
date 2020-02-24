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

time.sleep(2)
all_plans = driver.find_element_by_xpath(
    '//*[@id="mainForm:j_id_x:tbody_element"]')
rows = all_plans.find_elements_by_css_selector('tr')
for index, row in enumerate(rows):
    col = row.find_elements_by_css_selector('td')[0]
    semester = col.find_element_by_css_selector('h5')
    print(str(index) + ') ' + semester.text)

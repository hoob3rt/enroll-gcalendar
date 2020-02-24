import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

DRIVER = None


def connect():
    global DRIVER
    options = Options()
    options.headless = True
    DRIVER = webdriver.Firefox(options=options)
    print('headless Firefox initialized')
    print('connecting to http://enroll-me.iiet.pl/')
    DRIVER.get('http://enroll-me.iiet.pl/')


def rest():
    print('fetching semesters')
    time.sleep(2)
    content = DRIVER.find_element_by_xpath(
        '/html/body/div[2]/div[2]/form/div[4]/div/div/button[2]')
    content.click()

    login = DRIVER.find_element_by_xpath('//*[@id="student_username"]')
    password = DRIVER.find_element_by_xpath('//*[@id="student_password"]')
    login.send_keys("")
    password.send_keys("")
    login_button = DRIVER.find_element_by_xpath(
        '/html/body/div/div[2]/div/form/div[2]/input')
    login_button.click()

    enrollment_button = DRIVER.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div[2]/a')
    enrollment_button.click()

    time.sleep(2)
    all_plans = DRIVER.find_element_by_xpath(
        '//*[@id="mainForm:j_id_x:tbody_element"]')
    rows = all_plans.find_elements_by_css_selector('tr')
    semesters = {}
    for index, row in enumerate(rows):
        col = row.find_elements_by_css_selector('td')[0]
        semester = col.find_element_by_css_selector('h5')
        semesters[index] = (semester.text, row)
        print(str(index) + ') ' + semester.text)

    print('select semester index')
    selected_semester_index = int(input())
    try:
        selected_semester = [semesters[selected_semester_index]
                             for semester in semesters]
    except IndexError:
        print('please select correct semester index')
    number = selected_semester[0][0].split(' ')[0]
    print(number)
    for index in semesters:
        if semesters[index][0].split(
            ' ')[0] == number and int(semesters[index][0].split(
                ' ')[1]) == int(selected_semester[0][0].split(' ')[1])-2:
            print('elo warunki smieciu')

if __name__ == "__main__":
    connect()
    rest()
    pass

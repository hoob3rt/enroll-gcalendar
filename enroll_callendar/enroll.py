import time
from sys import maxsize

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

DRIVER = None
DAYS_LOCATIONS = {}


# TODO zmienic stringi na enkapsulacje zmiennych
# TODO add wait until available


def connect():
    '''
        establish connection to enroll-me.iiet.pl
    '''
    global DRIVER
    options = Options()
    options.headless = True
    DRIVER = webdriver.Firefox(options=options)
    # DRIVER = webdriver.Firefox()
    print('headless Firefox initialized')
    print('connecting to http://enroll-me.iiet.pl/')
    DRIVER.get('http://enroll-me.iiet.pl/')


def get_day_locations():
    '''
        TODO
    '''
    global DAYS_LOCATIONS
    DAYS_LOCATIONS['monday'] = {
        'start': int(DRIVER.find_elements_by_class_name(
            'fc-mon')[-1].location['x']),
        'middle': int(DRIVER.find_elements_by_class_name(
            'fc-mon')[-1].location['x']) + int(
                DRIVER.find_elements_by_class_name(
                    'fc-mon')[-1].size['width']/2)
    }
    DAYS_LOCATIONS['tuesday'] = {
        'start': int(DRIVER.find_elements_by_class_name(
            'fc-tue')[-1].location['x']),
        'middle': int(DRIVER.find_elements_by_class_name(
            'fc-tue')[-1].location['x']) + int(
                DRIVER.find_elements_by_class_name(
                    'fc-tue')[-1].size['width']/2)
    }
    DAYS_LOCATIONS['wednesday'] = {
        'start': int(DRIVER.find_elements_by_class_name(
            'fc-wed')[-1].location['x']),
        'middle': int(DRIVER.find_elements_by_class_name(
            'fc-wed')[-1].location['x']) + int(
                DRIVER.find_elements_by_class_name(
                    'fc-wed')[-1].size['width']/2)
    }
    DAYS_LOCATIONS['thursday'] = {
        'start': int(DRIVER.find_elements_by_class_name(
            'fc-thu')[-1].location['x']),
        'middle': int(DRIVER.find_elements_by_class_name(
            'fc-thu')[-1].location['x']) + int(
                DRIVER.find_elements_by_class_name(
                    'fc-thu')[-1].size['width']/2)
    }
    DAYS_LOCATIONS['friday'] = {
        'start': int(DRIVER.find_elements_by_class_name(
            'fc-fri')[-1].location['x']),
        'middle':
        int(DRIVER.find_elements_by_class_name(
            'fc-fri')[-1].location['x']) + int(
                DRIVER.find_elements_by_class_name(
                    'fc-fri')[-1].size['width']/2)
    }


def find_class_day(class_location):
    '''
        class loction is never the same as day location due to responsive
        padding
        finding class's day requires fidning minimum distance from
        class_location to each day_location
    '''
    min_distance = maxsize
    class_day = ''
    for day in DAYS_LOCATIONS:
        day_location_start = DAYS_LOCATIONS[day]['start']
        day_location_middle = DAYS_LOCATIONS[day]['middle']
        if abs(day_location_start - class_location) < min_distance:
            min_distance = abs(day_location_start - class_location)
            class_day = day
        if abs(day_location_middle - class_location) < min_distance:
            min_distance = abs(day_location_middle - class_location)
            class_day = day
    return class_day


def get_classes_from_semester(selected_semester, semesters, warunki,
                              all_classes):
    number = selected_semester[0].split(' ')[0]
    for index in semesters:
        if semesters[index][0].split(
                ' ')[0] == number and int(semesters[index][0].split(
                    ' ')[1]) == int(selected_semester[0].split(' ')[1])-2:
            warunki.append((semesters[index][0], semesters[index][1]))
    btn = selected_semester[1].find_elements_by_css_selector('td')[-1]
    b = btn.find_element_by_css_selector('div')
    b.click()
    time.sleep(2)
    lessons = DRIVER.find_elements_by_class_name('fc-event-inner')
    for lesson in lessons:
        get_day_locations()

        head = lesson.find_element_by_class_name('fc-event-head')
        date = head.find_element_by_class_name('fc-event-time')
        content = lesson.find_element_by_class_name('fc-event-content')
        title = content.find_element_by_class_name('fc-event-title')
        date = date.text.strip()
        classname = title.text.split(',')[0].strip()
        dude = title.text.split(',')[1].strip()
        try:
            room = title.text.split(',')[2].strip()
        except IndexError:
            room = dude
            dude = ''
        try:
            class_type = title.text.split(',')[3].strip().split('-')[-1]
        except IndexError:
            class_type = room.split('-')[-1].strip()
            room = room.split('-')[0].strip()
        all_classes.append((date, classname, dude, room, class_type,
                            find_class_day(lesson.location['x'])))


def click_enrollment_button():
    '''
        return to enrollment page
    '''
    enrollment_button = DRIVER.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div[2]/a')
    enrollment_button.click()


def login(username, password):
    '''
        sign in  with accounts.iiet.pl

        :username: user's username
        :password: user's password
    '''
    sign_in_with_accoutns_iet_button = DRIVER.find_element_by_xpath(
        '/html/body/div[2]/div[2]/form/div[4]/div/div/button[2]')
    sign_in_with_accoutns_iet_button.click()
    login_box = DRIVER.find_element_by_xpath('//*[@id="student_username"]')
    password_box = DRIVER.find_element_by_xpath('//*[@id="student_password"]')
    login_box.send_keys(username)
    password_box.send_keys(password)
    login_button = DRIVER.find_element_by_xpath(
        '/html/body/div/div[2]/div/form/div[2]/input')
    login_button.click()


def fetch_available_semesters(print_available_semesters=False):
    all_plans = DRIVER.find_element_by_xpath(
        '//*[@id="mainForm:j_id_x:tbody_element"]')
    rows = all_plans.find_elements_by_css_selector('tr')
    semesters = {}
    for index, row in enumerate(rows):
        col = row.find_elements_by_css_selector('td')[0]
        semester = col.find_element_by_css_selector('h5')
        semesters[index] = (semester.text, row)
        if print_available_semesters:
            print(str(index) + ') ' + semester.text)
    return semesters


def get_classes_from_selected_semesters(username, password):
    all_classes = []
    warunki = []

    time.sleep(2)
    print('fetching semesters')
    time.sleep(1)
    login(username, password)
    click_enrollment_button()
    time.sleep(2)
    semesters = fetch_available_semesters(print_available_semesters=True)
    try:
        selected_semester_index = int(input('select semester index: '))
    except ValueError:
        raise Exception('no semester selected')
    try:
        selected_semester = list(semesters.values())[selected_semester_index]
    except IndexError:
        print('please select correct semester index\n')
    get_classes_from_semester(selected_semester, semesters, warunki,
                              all_classes)
    if len(warunki) > 0:
        for index, warunek in enumerate(warunki):
            print(str(index) + ') ' + warunek[0])
        try:
            selected_semester_index = int(input(
                'select warunek to exclude(empty excludes none): '))
        except ValueError:
            selected_semester_index = None
        if selected_semester_index is not None:
            del warunki[selected_semester_index]
        click_enrollment_button()
        time.sleep(1)
        semesters = fetch_available_semesters()
        for warunek in warunki:
            for semester in semesters:
                if warunek[0] == semesters[semester][0]:
                    get_classes_from_semester(semesters[semester],
                                              semesters, warunki, all_classes)
    return all_classes


def close_driver():
    DRIVER.close()


def main(username, password):
    connect()
    get_classes_from_selected_semesters(username, password)
    close_driver()

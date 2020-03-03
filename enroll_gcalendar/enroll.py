#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    enroll-gcalendar.enroll
    ~~~~~~~~~~~~~~~~~~~~~~

    contains plan fetching functions

    :copyright: (c) 2020 by Hubert Pelczarski
    :license: MIT, see LICENSE for more details.
"""

import sys

import selenium.webdriver.firefox
import selenium.webdriver.chrome
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        WebDriverException)

DRIVER = None
DAYS_LOCATIONS = {}


def connect(timeout, driver_name=None):
    """
        establish connection to enroll-me.iiet.pl
    """
    global DRIVER
    if driver_name is None:
        try:
            options = selenium.webdriver.firefox.options.Options()
            options.headless = True
            DRIVER = webdriver.Firefox(options=options)
            print('headless Firefox initialized')
        except WebDriverException:
            print('firefox geckodriver not found')
        if DRIVER is None:
            try:
                options = selenium.webdriver.chrome.options.Options()
                options.headless = True
                DRIVER = webdriver.Chrome(options=options)
                print('headless Chrome initialized')
            except WebDriverException:
                print('chromedriver not found')
    elif driver_name == 'chrome':
        try:
            options = selenium.webdriver.chrome.options.Options()
            options.headless = True
            DRIVER = webdriver.Chrome(options=options)
            print('headless Chrome initialized')
        except WebDriverException:
            print('chromedriver not found')
    elif driver_name == 'firefox':
        try:
            options = selenium.webdriver.firefox.options.Options()
            options.headless = True
            DRIVER = webdriver.Firefox(options=options)
            print('headless Firefox initialized')
        except WebDriverException:
            print('firefox geckodriver not found')
    if DRIVER is None:
        raise Exception('no webdriver found, refer to help or README.md')
    DRIVER.implicitly_wait(timeout)
    print('connecting to http://enroll-me.iiet.pl/')
    DRIVER.get('http://enroll-me.iiet.pl/')


def get_day_locations():
    """
        fetches location of all weekdays from enroll-me.iiet.pl
    """
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


def find_lesson_day(lesson_location):
    """
        lesson loction is never the same as day location due to responsive
        padding
        finding lesson's day requires fidning minimum distance from
        lesson_location to each day_location
    """
    min_distance = sys.maxsize
    lesson_day = ''
    for day in DAYS_LOCATIONS:
        day_location_start = DAYS_LOCATIONS[day]['start']
        day_location_middle = DAYS_LOCATIONS[day]['middle']
        if abs(day_location_start - lesson_location) < min_distance:
            min_distance = abs(day_location_start - lesson_location)
            lesson_day = day
        if abs(day_location_middle - lesson_location) < min_distance:
            min_distance = abs(day_location_middle - lesson_location)
            lesson_day = day
    return lesson_day


def format_time_to_24_format(lesson_time_block):
    """
        formats enroll's time format to google's 24h format
    """
    lesson_time = lesson_time_block.text.strip().replace(' ', '')
    description = ''
    if not lesson_time[-1].isdigit():
        description = lesson_time[-1]
        lesson_time = (lesson_time[0:-1])
    diff = DRIVER.find_element_by_class_name('fc-slot20')
    starting_hour = lesson_time.split('-')[0]
    ending_hour = lesson_time.split('-')[1]

    # start of enroll square
    if lesson_time_block.location['y'] < diff.location['y']:
        hour = starting_hour.split(':')[0]
        if len(hour) < 2:
            hour = f'0{hour}'
        starting_hour = hour + ':' + starting_hour.split(':')[1]
    else:
        hour = starting_hour.split(':')[0]
        hour = str(12 + int(hour))
        starting_hour = hour + ':' + starting_hour.split(':')[1]

    # end of enroll square
    if (lesson_time_block.location['y']+lesson_time_block.size['height'] <
            diff.location['y']):
        hour = ending_hour.split(':')[0]
        if len(hour) < 2:
            hour = f'0{hour}'
        ending_hour = hour + ':' + ending_hour.split(':')[1]
    else:
        hour = ending_hour.split(':')[0]
        hour = str(12 + int(hour))
        ending_hour = hour + ':' + ending_hour.split(':')[1]
    lesson_time = f'{starting_hour}-{ending_hour}'
    return lesson_time, description


def get_lessons_from_semester(selected_semester, semesters, overdue_lessons,
                              all_lessons):
    """
        fetches all lessons from selected semester
    """
    number = selected_semester[0].split(' ')[0]
    for index in semesters:
        if semesters[index][0].split(
                ' ')[0] == number and int(semesters[index][0].split(
                    ' ')[1]) == int(selected_semester[0].split(' ')[1])-2:
            overdue_lessons.append((semesters[index][0], semesters[index][1]))
    semester_buttons = selected_semester[1].find_elements_by_css_selector(
        'td')[-1]
    your_schedule_button = semester_buttons.find_element_by_css_selector('div')
    your_schedule_button.click()
    lessons = DRIVER.find_elements_by_class_name('fc-event-inner')
    for lesson in lessons:
        get_day_locations()
        lesson_header = lesson.find_element_by_class_name('fc-event-head')
        lesson_content = lesson.find_element_by_class_name('fc-event-content')

        title = lesson_content.find_element_by_class_name('fc-event-title')
        lessonname = title.text.split(',')[0].strip()
        lecturer = title.text.split(',')[1].strip()
        lesson_time_block = lesson_header.find_element_by_class_name(
            'fc-event-time')
        lesson_time, description = format_time_to_24_format(lesson_time_block)
        try:
            room = title.text.split(',')[2].strip()
        except IndexError:
            room = lecturer
            lecturer = ''
        try:
            lesson_type = title.text.split(
                ',')[3].strip().split('-')[-1].strip()
        except IndexError:
            lesson_type = room.split('-')[-1].strip()
            room = room.split('-')[0].strip()
        all_lessons.append((lesson_time, lessonname, lecturer, room,
                            lesson_type, description,
                            find_lesson_day(lesson.location['x'])))


def click_enrollment_button():
    """
        return to enrollment page
    """
    try:
        enrollment_button = DRIVER.find_element_by_xpath(
            '/html/body/div[1]/div/div[2]/div[2]/a')
        enrollment_button.click()
    except NoSuchElementException:
        print(
            'fetching semesters failed, possibly due to wrong login info')
        sys.exit(1)


def login(username, password):
    """
        sign in  with accounts.iiet.pl

        :username: user's username
        :password: user's password
    """
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
    """
        fetches all available semesters from enrollment page
    """
    all_plans = DRIVER.find_element_by_xpath(
        '//*[@id="mainForm:j_id_x:tbody_element"]')
    rows = all_plans.find_elements_by_css_selector('tr')
    semesters = {}
    for index, row in enumerate(rows):
        col = row.find_elements_by_css_selector('td')[0]
        semester = col.find_element_by_css_selector('h5')
        semesters[index] = (semester.text, row)
        if print_available_semesters:
            print(f'{index}) {semester.text}')
    return semesters


def get_lessons_from_selected_semesters(username, password):
    """
        fetches all lessons from selected semesters
    """
    all_lessons = []
    overdue_lessons = []
    print('fetching semesters')
    login(username, password)
    click_enrollment_button()
    semesters = fetch_available_semesters(print_available_semesters=True)
    try:
        selected_semester_index = int(input('select semester index: '))
    except ValueError:
        raise Exception('no semester selected')
    try:
        selected_semester = list(semesters.values())[selected_semester_index]
    except IndexError:
        print('please select correct semester index\n')
    get_lessons_from_semester(selected_semester, semesters, overdue_lessons,
                              all_lessons)
    if len(overdue_lessons) > 0:
        for index, overdue_lesson in enumerate(overdue_lessons):
            print(f'{index}) {overdue_lesson[0]}')
        try:
            selected_semester_index = int(input(
                'select overdue semester to exclude(empty excludes none): '))
        except ValueError:
            selected_semester_index = None
        if selected_semester_index is not None:
            del overdue_lessons[selected_semester_index]
        click_enrollment_button()
        semesters = fetch_available_semesters()
        for overdue_lesson in overdue_lessons:
            for semester in semesters:
                if overdue_lesson[0] == semesters[semester][0]:
                    get_lessons_from_semester(semesters[semester],
                                              semesters, overdue_lessons,
                                              all_lessons)
    return all_lessons


def close_driver():
    """
        closes driver
    """
    DRIVER.close()

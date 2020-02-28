#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    enroll-calendar.schedule_preparator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    set of functions preparing for conversion to google calendar

    :copyright: (c) 2020 by Hubert Pelczarski
    :license: LICENSE_NAME, see LICENSE for more details.
"""

import datetime
import os

from enroll import DAYS_LOCATIONS


def sort_lessons_by_day(all_lessons):
    """
        sorts lessons by day
    """
    sorted_lessons = []
    for day in DAYS_LOCATIONS:
        for lesson in all_lessons:
            if lesson[-1] == day:
                sorted_lessons.append(lesson)
    return sorted_lessons


def print_lessons_by_day(all_lessons, sort_lessons=False, print_indices=False):
    """
        prints lessons day by day
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # clear screen
    if sort_lessons:
        all_lessons = sort_lessons_by_day(all_lessons)
    print('current plan:\n')
    for day in DAYS_LOCATIONS:
        print(day.capitalize())
        for index, lesson in enumerate(all_lessons):
            if lesson[-1] == day:
                lesson_view = ''
                if print_indices:
                    lesson_view += f'{index})'
                lesson_view += (f'{lesson[0]} {lesson[1]}-{lesson[4]}'
                                f' {lesson[5]} {lesson[2]} {lesson[3]}')
                print(lesson_view)
        print('')


def remove_lessons(all_lessons):
    """
        removes all lessons selected by user
    """
    choice = input('select index to remove, -1 removes all lecutres(W): ')
    if int(choice) == -1:
        all_lessons = [lesson for lesson in all_lessons if lesson[-3] != 'W']
        print_lessons_by_day(
            all_lessons, sort_lessons=True, print_indices=True)
    else:
        if int(choice) > len(all_lessons):
            print('provided index too big')
        else:
            all_lessons = [lesson for index, lesson in enumerate(all_lessons)
                           if index != int(choice)]
            print_lessons_by_day(
                all_lessons, sort_lessons=True, print_indices=True)
    continue_deleting = input('continue removing? [y/N] ')
    if continue_deleting.lower() == 'y':
        all_lessons = remove_lessons(all_lessons)
    return all_lessons


def find_next_weekday(start_date, weekday=0):
    """
        finds next weekday from provided start_date,
        defaults to search for monday
        :start_date: date to start the search from
        :weekday: day of week to search for, 0:Monday, 1:Tueseday...
    """
    while start_date.weekday() != weekday:
        start_date += datetime.timedelta(days=1)
    return start_date


def convert_to_gcalendar_event(start_date, end_date, lesson):
    """
        convert single lesson into google calendar format
        :lesson: lesson to convert
        :start_date: start date of lesson
        :end_date: end date of lesson
    """
    index = next(index for index, key in enumerate(
        DAYS_LOCATIONS) if key == lesson[-1])
    start_date_date = datetime.datetime.strftime((find_next_weekday(start_date,
                                                                    index)),
                                                 "%Y-%m-%d")
    end_date_date = datetime.datetime.strftime(end_date, "%Y%m%d")
    start_date_start_time = lesson[0].split('-')[0]
    start_date_end_time = lesson[0].split('-')[1]
    if lesson[-2] != '':
        summary = f'{lesson[1]} - {lesson[-2]}'
    else:
        summary = lesson[1]
    event = {
        'summary': f'{summary}',
        'location': f'{lesson[-4]}',
        'description': f'lecturer: {lesson[2]}',
        'start': {
            'dateTime': f'{start_date_date}T{start_date_start_time}:00',
            'timeZone': 'Europe/Warsaw',
        },
        'end': {
            'dateTime': f'{start_date_date}T{start_date_end_time}:00',
            'timeZone': 'Europe/Warsaw'
        },
        'recurrence': [
            f'RRULE:FREQ=WEEKLY;UNTIL={end_date_date}T000000Z',
        ]
    }
    return event

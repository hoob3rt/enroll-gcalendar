#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    enroll-calendar.convert_plan
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    sets up cli & contains main convertion function

    :copyright: (c) 2020 by Hubert Pelczarski
    :license: LICENSE_NAME, see LICENSE for more details.
"""

import argparse
import datetime
import sys
from getpass import getpass

import gcalendar_handler
from enroll import close_driver, connect, get_lessons_from_selected_semesters
from schedule_preparator import (convert_to_gcalendar_event,
                                 print_lessons_by_day, remove_lessons)


def convert_plan():
    """
        converts enroll plan to google calendar
    """
    timeout, username, driver, start_date, end_date, dry_run = setup_cli()
    creds = gcalendar_handler.evaluate_credentials()
    if timeout is None or not timeout.isdigit():
        timeout = 5
    if driver in ('chrome', 'firefox'):
        connect(timeout, driver)
    else:
        connect(timeout)
    if username is None:
        username = input('enter enroll username: ')
    else:
        print(f'username: {username}')
    password = getpass('enter enroll password: ')
    all_lessons = get_lessons_from_selected_semesters(username, password)
    print_lessons_by_day(all_lessons, sort_lessons=True, print_indices=True)
    remove = input('do you want to remove any lessons?[y/N] ')
    if remove.lower() == 'y':
        all_lessons = remove_lessons(all_lessons)
    if dry_run:
        print('dry run finished')
    else:
        add_to_calendar = input(
            'do you want to add above plan to your google calendar?[y/N] ')
        if add_to_calendar.lower() == 'y':
            if start_date is None:
                start_date = input(
                    'enter semester start date (format YYYY-MM-DD): ')
            if end_date is None:
                end_date = input(
                    'enter semester end date (format YYYY-MM-DD): ')
            for lesson in all_lessons:
                try:
                    event = (convert_to_gcalendar_event(
                        datetime.datetime.strptime(start_date, '%Y-%m-%d'),
                        datetime.datetime.strptime(end_date, '%Y-%m-%d'),
                        lesson))
                except ValueError:
                    print('wrong start or end date format')
                    sys.exit(1)
                gcalendar_handler.create_event(event, creds)

    close_driver()


def setup_cli():
    """
        initializes command line arguments
    """
    parser = argparse.ArgumentParser(
        description='Convert enroll plan to google calendar')
    parser.add_argument('-t', '--timeout',
                        help=('timeout for fetches, set hight value with '
                              'slower connections (default: 5)'))
    parser.add_argument('-u', '--username',
                        help=('provide enroll username before running script'))
    parser.add_argument('-d', '--driver',
                        help=('choose driver before running script '
                              '(available values: chrome, firefox)'))
    parser.add_argument('-s', '--start-date',
                        help=('choose start_date before running script '
                              '(format: YYYY-MM-DD)'))
    parser.add_argument('-e', '--end-date',
                        help=('choose end_date before running script '
                              '(format: YYYY-MM-DD)'))
    parser.add_argument('-dr', '--dry-run', default=False, action='store_true',
                        help=('run script without convertion'))
    args = parser.parse_args()
    return (args.timeout, args.username, args.driver, args.start_date,
            args.end_date, args.dry_run)


if __name__ == "__main__":
    convert_plan()

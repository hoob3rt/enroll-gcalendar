import datetime
import os

from enroll import DAYS_LOCATIONS


def sort_classes_by_day(all_classes):
    """
        sorts classes by day
    """
    sorted_classes = []
    for day in DAYS_LOCATIONS:
        for clas in all_classes:
            if clas[-1] == day:
                sorted_classes.append(clas)
    return sorted_classes


def print_classes_by_day(all_classes, sort_classes=False, print_indices=False):
    """
        prints classes day by day
    """
    os.system('cls' if os.name == 'nt' else 'clear')  # clear screen
    if sort_classes:
        sort_classes_by_day(all_classes)
    print('current plan:\n')
    for day in DAYS_LOCATIONS:
        print(day.capitalize())
        for index, clas in enumerate(all_classes):
            if clas[-1] == day:
                if print_indices:
                    print(f'{index}) {clas[0:-1]}')
                else:
                    print(clas[0:-1])
        print('')


def remove_classes(all_classes):
    """
        removes all classes selected by user
    """
    choice = input('select index to remove, -1 removes all lecutres(W): ')
    if int(choice) == -1:
        all_classes = [clss for clss in all_classes if clss[-2] != 'W']
        print_classes_by_day(
            all_classes, sort_classes=True, print_indices=True)
    else:
        if int(choice) > len(all_classes):
            print('provided index too big')
        else:
            all_classes = [clss for index, clss in enumerate(all_classes)
                           if index != int(choice)]
            print_classes_by_day(
                all_classes, sort_classes=True, print_indices=True)

    continue_deleting = input('continue removing? [y/N]')
    if continue_deleting.lower() == 'y':
        all_classes = remove_classes(all_classes)
    return all_classes


def find_next_weekday(start_date, weekday=0):
    """
        finds next weekday from provided start_date,
        defaults to search for monday
        :start_date: date to start the search from 
        :weekday: day of week to search for, 0:Monday, 1:Tueseday....
    """
    while start_date.weekday() != weekday:
        start_date += datetime.timedelta(days=1)
    return start_date


def convert_to_gcalendar_format(all_classes):
    pass

from enroll import connect, get_classes_from_selected_semesters, close_driver
from getpass import getpass


if __name__ == "__main__":
    connect()
    username = input('enter username: ')
    password = getpass('enter password: ')
    get_classes_from_selected_semesters(username, password)
    close_driver()

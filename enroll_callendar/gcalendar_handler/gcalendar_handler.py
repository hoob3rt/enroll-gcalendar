#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    enroll-calendar.gcalendar_handler.gcalendar_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2020 by Hubert Pelczarski
    :license: LICENSE_NAME, see LICENSE for more details.
"""

import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying thesescopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']


def evaluate_credentials():
    """
        check existance of google credentials

        The file token.pickle stores the user's access and refresh tokens,
        and is created automatically when the authorization flow completes
        for the first time.
    """
    creds = None
    script_dir = os.path.dirname(os.path.realpath(__file__))
    rel_path = '../../google_credentials'
    abs_file_path = os.path.join(script_dir, rel_path)
    if os.path.exists(os.path.join(abs_file_path, 'token.pickle')):
        with open(os.path.join(abs_file_path, 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)
            print('google credentials found')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if os.path.exists(os.path.join(abs_file_path, 'credentials.json')):
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(abs_file_path, 'credentials.json'), SCOPES)
                creds = flow.run_local_server(port=0)
                print('google credentials found')
            else:
                raise Exception("no google credentials found, place them in "
                                "google_credentials directory")
        # Save the credentials for the next run
        with open(os.path.join(abs_file_path, 'token.pickle'), 'wb') as token:
            pickle.dump(creds, token)
    return creds


def create_event(event, creds):
    """
        Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
    """
    service = build('calendar', 'v3', credentials=creds)
    name = event['summary']
    print(f'creating {name}')
    event = service.events().insert(calendarId='primary', body=event).execute()

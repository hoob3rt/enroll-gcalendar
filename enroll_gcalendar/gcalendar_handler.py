#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    enroll-gcalendar.gcalendar_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2020 by Hubert Pelczarski
    :license: MIT, see LICENSE for more details.
"""

import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying thesescopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']


def get_credentials(path):
    """
        check existance of google credentials

        The file token.pickle stores the user's access and refresh tokens,
        and is created automatically when the authorization flow completes
        for the first time.
    """
    creds = None
    if os.path.exists(os.path.join(path, 'token.pickle')):
        with open(os.path.join(path, 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)
            print('google credentials found')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if os.path.exists(os.path.join(path, 'credentials.json')):
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(path, 'credentials.json'), SCOPES)
                creds = flow.run_local_server(port=0)
                print('google credentials found')
            else:
                raise Exception("no google credentials found, place them in "
                                f"{path}")
        # Save the credentials for the next run
        with open(os.path.join(path, 'token.pickle'), 'wb') as token:
            pickle.dump(creds, token)
    return creds


def evaluate_credentials(path=None):
    """
        fetch google credentials from provided path
    """
    creds = None
    if path is None:
        path = '../google_credentials'
    creds = get_credentials(path)
    return creds


def create_event(event, creds):
    """
        creates google calendar event
    """
    service = build('calendar', 'v3', credentials=creds)
    name = event['summary']
    print(f'creating {name}')
    event = service.events().insert(calendarId='primary', body=event).execute()

from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GCalManager:
    def __init__(self, calendar_id):
        self.calendar_id = calendar_id
        self.creds = None
        self.service = None
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('calendar', 'v3', credentials=self.creds)

    def set_calendar(self, calendar_id):
        self.calendar_id = calendar_id

    def create_event(self, name, desc, start_time, end_time, date):
        event = None
        try:
            event = {
                'summary': name,
                #'location': 'Parc TecnoCampus Mataró-Maresme, Carrer d\'Ernest Lluch, 32, 08302 Mataró, Barcelona',
                'description': desc,
                'start': {
                    'dateTime': date + 'T' + start_time,
                    'timeZone': 'Europe/Madrid',
                },
                'end': {
                    'dateTime': date + 'T' + end_time,
                    'timeZone': 'Europe/Madrid',
                },
            }

            event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
        except HttpError as error:
            print('An error occurred: %s' % error)
        except:
            print('Unknown error')

        return event
    
    def get_next_events(self, n):
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = self.service.events().list(calendarId=self.calendar_id, timeMin=now,
                                              maxResults=n, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events


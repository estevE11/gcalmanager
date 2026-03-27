from __future__ import print_function

import datetime
import os.path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GCalManager:
    def __init__(self, calendar_id):
        self.calendar_id = calendar_id
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        service_account_path = os.path.join(script_dir, 'translator-294716-fae0969f6d9b.json')

        self.creds = Credentials.from_service_account_file(service_account_path, scopes=SCOPES)
        self.service = build('calendar', 'v3', credentials=self.creds)

    def set_calendar(self, calendar_id):
        self.calendar_id = calendar_id

    def create_event(self, name, desc, start_time, end_time, date, location=''):
        event = None
        try:
            event = {
                'summary': name,
                'location': location,
                'description': desc,
                'start': {
                    'dateTime': date + 'T' + start_time + ":00",
                    'timeZone': 'Europe/Madrid',
                },
                'end': {
                    'dateTime': date + 'T' + end_time + ":00",
                    'timeZone': 'Europe/Madrid',
                },
            }

            print(event)

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

    def get_event(self, event_id):
        event = self.service.events().get(calendarId=self.calendar_id, eventId=event_id).execute()
        return event

    def delete_event(self, event_id):
        deleted = self.service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()
        return deleted

    def move_event(self, event_id, destination_calendar_id):
        moved = self.service.events().move(calendarId=self.calendar_id, eventId=event_id, destination=destination_calendar_id).execute()
        return moved

    def quickAdd(self, text):
        created = self.service.events().quickAdd(calendarId=self.calendar_id, text=text).execute()
        return created

    def update_event(self, event_id, body):
        updated = self.service.events().quickAdd(calendarId=self.calendar_id, evendId=event_id, body=body).execute()
        return updated

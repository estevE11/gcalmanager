from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the required API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GCalManager:
    def __init__(self, calendar_id):
        self.calendar_id = calendar_id
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Handles Google Calendar API authentication and token management."""
        token_path = './token.json'
        credentials_path = './credentials.json'

        try:
            # Load existing credentials if available
            if os.path.exists(token_path):
                self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)

            # Refresh or obtain new credentials if needed
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    # Start OAuth flow if no valid credentials exist
                    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                    self.creds = flow.run_local_server(port=8080)

                # Save the new credentials
                with open(token_path, 'w') as token:
                    token.write(self.creds.to_json())

            # Initialize the Google Calendar API service
            self.service = build('calendar', 'v3', credentials=self.creds)

        except Exception as e:
            print(f"Error during authentication: {e}")
            self.service = None

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
                    'timeZone': 'GMT+01:00',
                },
                'end': {
                    'dateTime': date + 'T' + end_time + ":00",
                    'timeZone': 'GMT+01:00',
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

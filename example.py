from gcalmanager import GCalManager

calendar_id = "c_6qimrdfv0qrflqq864unsolkis@group.calendar.google.com"

gcal = GCalManager(calendar_id)
gcal.create_event("Test event name", "Test description", "12:00", "17:00", "2022-12-01")
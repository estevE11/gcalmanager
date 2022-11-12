# GCalManager
GCalManager is NOT a good Google Calendar API Python implementation.

## Example code
```python
from gcalmanager import GCalManager

calendar_id = "c_6qimrdfv0qrf@group.calendar.google.com" # not an actual calendar id just an example

gcal = GCalManager(calendar_id)
gcal.create_event("Test event name", "Test description", "12:00", "17:00", "2022-12-01")
```

## Features
- Get next events
- Get event
- Create event
- Create event based on text
- Update event
- Delete event
- Move event to another calendar

It currently only supports creating an event because is the only one I needed 🤡
import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def get_upcoming_events(credentials: Credentials):
    service = build("calendar", "v3", credentials=credentials)

    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time

    calendar_list = service.calendarList().list().execute()
    calendars = calendar_list.get("items", [])
    all_events = []

    for calendar in calendars:
        if "pl.polish" in calendar["id"].lower():
            continue
        else:
            calendar_id = calendar["id"]
            events_result = service.events().list(calendarId=calendar_id, timeMin=now, maxResults=3, singleEvents=True,
                                                  orderBy="startTime").execute()
            events = events_result.get("items", [])

            for event in events:
                event_summary = event.get("summary", "No Title")
                start = event["start"].get("dateTime", event["start"].get("date")).split("+").pop(0)
                end = event["end"].get("dateTime", event["end"].get("date")).split("+").pop(0)
                location = event.get("location", "None")

                event_dict = {
                    "summary": event_summary,
                    "start": start,
                    "end": end,
                    "location": location
                }
                all_events.append(event_dict)

    return all_events
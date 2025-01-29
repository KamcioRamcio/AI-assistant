from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def get_upcoming_events(credentials: Credentials):
    service = build("calendar", "v3", credentials=credentials)

    now = datetime.utcnow()
    start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0)
    end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)

    # Format the times to ISO 8601 (required by the Google Calendar API)
    time_min = start_of_day.isoformat() + "Z"  # Add 'Z' to indicate UTC time
    time_max = end_of_day.isoformat() + "Z"

    calendar_list = service.calendarList().list().execute()
    calendars = calendar_list.get("items", [])
    all_events = []

    for calendar in calendars:
        if "pl.polish" in calendar["id"].lower():
            continue
        else:
            calendar_id = calendar["id"]
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=3,
                singleEvents=True,
                orderBy="startTime"
            ).execute()
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


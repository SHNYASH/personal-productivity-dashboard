"""
This script extracts event data from multiple Google Calendars
            using the google calendar API.
"""

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_events():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  calendars = ["4813dfca9a84012600079d3c18251afefb720aaccc784a5da050e6901996a50e@group.calendar.google.com",
"eb8b319f4e3975c1b8ae6451d1bd914e335a07947a679b46771cd55bc9be5df3@group.calendar.google.com",
"5ade13f642e0134095ad4a8c68c2a504a5790d178e2a40375bfbbfaf1153928c@group.calendar.google.com",
"e3394ec48c4ec3c71a70f2e7630a66158764a99462fcbc01da6b05444192c6ac@group.calendar.google.com"
]
  events = []
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    param_name = "timeMin"
    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    time_max = (datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days = 365)).isoformat()
    print("Getting the events")
    if os.path.exists("last_run"):
      with open("last_run") as f:
        raw_text = f.read()
        last_run_dt = datetime.datetime.fromisoformat(raw_text).isoformat()
        param_name = "updatedMin"
    else:
      print("last_run doesn't exist")
      last_run_dt = (datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days = 4*365)).isoformat()

  
    for cal_id in calendars:
        cal_meta = service.calendarList().get(calendarId=cal_id).execute()
        cal_name = cal_meta.get('summary', cal_id)
        print(f"Fetching from: {cal_name}")
        page_token = None
        while True:
          parameters = {
            "calendarId": cal_id,
            param_name: last_run_dt,
            "timeMax": time_max,
            "maxResults": 2500,
            "pageToken": page_token,
            "singleEvents": True,
            
          }
          # The API Request
          events_result = (service.events().list(**parameters).execute())

          current_events = events_result.get("items", [])

          # Omits all day events
          for event in current_events:
            if "dateTime" in event["start"]:
              event['calendar_name'] = cal_name
              events.append(event)
            else:
              continue

          page_token = events_result.get('nextPageToken')

          if not page_token:
            break

        print(f"Fetched {len(current_events)} events")
          
    if not events:
        print("No upcoming events found.")
        print(last_run_dt)
        return

  # Update last_run    
    with open("last_run", 'w') as f:
      f.write(now)

  # Event Counter
    print(f"Total events fetched: {len(events)}")
    return events
  
  # Error Message
  except HttpError as error:
    print(f"An error occurred: {error}")
    return []


if __name__ == "__main__":
  get_events()
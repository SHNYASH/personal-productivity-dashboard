"""
This script cleans event data fetched from google calendars,
             preparing it for a PostgreSQL database as part of a 
             personal productivity dashboard.
"""

import pandas as pd

def pandas_clean(events_data):
    staging_schema = ['id', 'status', 'created', 'updated', 'summary', 'sequence',
                        'calendar_name', 'creator_email', 'organizer_email', 'organizer_displayname', 'organizer_self',
                        'start_datetime', 'start_timezone', 'end_datetime', 'end_timezone', 'colorid', 'location', 'recurringeventid', 'description', 'duration']

    df = pd.json_normalize(events_data)
    df = df.rename(columns=lambda x: x.replace('.', '_').lower())
    df['start_datetime'] = pd.to_datetime(df['start_datetime'], utc=True)
    df['end_datetime'] = pd.to_datetime(df['end_datetime'], utc=True)
    duration = df['end_datetime'] - df['start_datetime']
    df['duration'] = duration.dt.total_seconds() / 60
    df['duration'] = df['duration'].fillna(0).astype(int)
    df = df.reindex(columns=staging_schema)

    return df

if __name__ == '__main__':
    events_data = [{'id': '45432tgr2', 'created': '2024-01-01T10:00:00Z', 'updated': '2024-01-01T10:00:00Z', 'summary': 'Test3 Event', 'organizer_self': True, 'start': {'dateTime': '2024-01-01T10:00:00Z', 'timezone': 'Malaysia'}, 'end': {'datetime': '2024-01-01T14:56:00Z', 'timezone': 'Malaysia'}}]
    print(pandas_clean(events_data))
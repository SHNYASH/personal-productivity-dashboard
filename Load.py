"""
This script loads the cleaned data into a postgres database
            to later be accessed by PowerBI.
"""

import pandas as pd
import sqlalchemy
import os
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASS")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

connection_url = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
engine = sqlalchemy.create_engine(connection_url)

def load_to_postgres(cleaned_data):
    df = cleaned_data
    upsert_sql = text("""INSERT INTO fact_events (
                      "id",
                      status,
                      created,
                      updated,
                      summary,
                      "sequence",
                      calendar_name,
                      creator_email,
                      organizer_email,
                      organizer_displayname,
                      organizer_self,
                      start_datetime,
                      start_timezone,
                      end_datetime,
                      end_timezone,
                      colorid,
                      "location",
                      description,
                      duration
                      )
                      SELECT 
                      "id",
                      status,
                      created::TIMESTAMPTZ,
                      updated::TIMESTAMPTZ,
                      summary,
                      "sequence",
                      calendar_name,
                      creator_email,
                      organizer_email,
                      organizer_displayname,
                      organizer_self,
                      start_datetime::TIMESTAMPTZ,
                      start_timezone,
                      end_datetime::TIMESTAMPTZ,
                      end_timezone,
                      colorid,
                      "location",
                      description,
                      duration
                      FROM stg_events_data
                      ON CONFLICT("id")
                      DO UPDATE SET
                      status = EXCLUDED.status,
                      created = EXCLUDED.created,
                      updated = EXCLUDED.updated,
                      summary = EXCLUDED.summary,
                      "sequence" = EXCLUDED.sequence,
                      calendar_name = EXCLUDED.calendar_name,
                      creator_email = EXCLUDED.creator_email,
                      organizer_email = EXCLUDED.organizer_email,
                      organizer_displayname = EXCLUDED.organizer_displayname,
                      organizer_self = EXCLUDED.organizer_self,
                      start_datetime = EXCLUDED.start_datetime,
                      start_timezone = EXCLUDED.start_timezone,
                      end_datetime = EXCLUDED.end_datetime,
                      end_timezone = EXCLUDED.end_timezone,
                      colorid = EXCLUDED.colorid,
                      "location" = EXCLUDED.location,
                      description = EXCLUDED.description,
                      duration = EXCLUDED.duration;""")
    try:
        df.to_sql('stg_events_data', con=engine, if_exists='replace', index=False, chunksize=500, method='multi')
        with engine.connect() as conn:
            print('Successfully connected!')
            conn.execute(upsert_sql)
            conn.commit()

    except Exception as e:
        print(f'An error has occured... {e}')


if __name__ == "__main__":
    staging_schema = ['id', 'status', 'created', 'updated', 'summary', 'sequence',
                        'calendar_name', 'creator_email', 'organizer_email', 'organizer_displayname', 'organizer_self',
                        'start_datetime', 'start_timezone', 'end_datetime', 'end_timezone', 'colorid', 'location', 'recurringeventid', 'description']
    test_data = pd.json_normalize([{'id': '45432tgr2', 'created': '2024-01-01T10:00:00Z', 'updated': '2024-01-01T10:00:00Z', 'summary': 'Test3 Event', 'organizer_self': True, 'start': {'dateTime': '2024-01-01T10:00:00Z', 'timezone': 'Malaysia'}, 'end': {'datetime': '2024-01-01T14:06:00Z', 'timezone': 'Malaysia'}}])
    test_data = test_data.rename(columns=lambda x: x.replace('.', '_').lower())
    test_data = test_data.reindex(columns=staging_schema)
    load_to_postgres(test_data)
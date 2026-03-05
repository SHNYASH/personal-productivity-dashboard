CREATE TABLE IF NOT EXISTS stg_events_data
(
    id text PRIMARY KEY,
    "status" double precision,
    created text,
    updated text,
    summary text,
    "sequence" double precision,
    calendar_name double precision,
    creator_email double precision,
    organizer_email double precision,
    organizer_displayname double precision,
    organizer_self boolean,
    start_datetime text,
    start_timezone text,
    end_datetime text,
    end_timezone text,
    colorid double precision,
    "location" double precision,
    recurringeventid double precision,
    "description" double precision
)
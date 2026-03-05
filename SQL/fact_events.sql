CREATE TABLE IF NOT EXISTS fact_events
(
    id text NOT NULL,
    status text,
    created timestamp with time zone,
    updated timestamp with time zone,
    summary text,
    sequence text,
    calendar_name text,
    creator_email text,
    organizer_email text,
    organizer_displayname text,
    organizer_self boolean,
    start_datetime timestamp with time zone,
    start_timezone text,
    end_datetime timestamp with time zone,
    end_timezone text,
    colorid text,
    location text,
    recurringeventid text,
    description text,
    duration integer,
    CONSTRAINT fact_events_pkey PRIMARY KEY (id)
);
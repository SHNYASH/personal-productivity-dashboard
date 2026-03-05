CREATE TABLE dim_date AS
WITH date_range AS (
    SELECT 
        COALESCE(MIN(start_datetime)::DATE, '2020-01-01'::DATE) as start_date,
        (CURRENT_DATE + INTERVAL '1 year')::DATE as end_date
    FROM fact_events
)
SELECT
    datum::DATE AS date_actual,
    EXTRACT(YEAR FROM datum) AS year,
    EXTRACT(MONTH FROM datum) AS month_num,
    TO_CHAR(datum, 'Month') AS month_name,
    EXTRACT(WEEK FROM datum) AS week,
	EXTRACT(DAY FROM datum) AS day_of_month, 
    TO_CHAR(datum, 'Day') AS day_of_week
FROM date_range, 
     generate_series(start_date, end_date, '1 day'::INTERVAL) AS datum;

-- Add the Primary Key to ensure Power BI recognizes unique rows
ALTER TABLE dim_date ADD PRIMARY KEY (date_actual);
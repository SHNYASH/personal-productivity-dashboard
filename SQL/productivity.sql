CREATE OR REPLACE VIEW productivity AS
SELECT 
    f.id, 
    f.summary, 
    f.sequence, 
    f.calendar_name, 
    f.start_datetime AS datetime, 
    d.year, 
    d.month_num, 
    d.month_name, 
    d.week, 
    d.day_of_month, 
    d.day_of_week, 
    f.location, 
    ROUND((f.duration::numeric / 60), 2) AS duration_hours
FROM fact_events AS f
LEFT JOIN dim_date AS d 
    ON f.start_datetime::DATE = d.date_actual
WHERE f.duration < (24 * 60) AND status LIKE ('confirmed')
ORDER BY f.start_datetime DESC;
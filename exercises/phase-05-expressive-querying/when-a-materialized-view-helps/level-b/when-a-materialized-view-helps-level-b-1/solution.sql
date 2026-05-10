DROP MATERIALIZED VIEW IF EXISTS events.hourly_event_counts;
CREATE MATERIALIZED VIEW events.hourly_event_counts AS
SELECT source_id, date_trunc('hour', occurred_at) AS hour_start, count(*) AS event_count
FROM events.events
GROUP BY source_id, date_trunc('hour', occurred_at);

SELECT source_id, hour_start, event_count
FROM events.hourly_event_counts
ORDER BY event_count DESC, source_id, hour_start
LIMIT 20;

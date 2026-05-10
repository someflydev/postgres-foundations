SELECT
    source_id,
    occurred_at,
    event_type,
    occurred_at - lag(occurred_at) OVER (PARTITION BY source_id ORDER BY occurred_at, id) AS since_previous_event
FROM events.events
ORDER BY source_id, occurred_at, id
LIMIT 40;

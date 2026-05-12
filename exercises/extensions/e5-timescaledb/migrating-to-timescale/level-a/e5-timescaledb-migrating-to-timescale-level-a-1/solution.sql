SELECT time_bucket('1 hour', occurred_at) AS bucket, count(*) AS events
FROM events.event_log_partitioned
WHERE occurred_at >= now() - INTERVAL '7 days'
GROUP BY bucket
ORDER BY bucket;

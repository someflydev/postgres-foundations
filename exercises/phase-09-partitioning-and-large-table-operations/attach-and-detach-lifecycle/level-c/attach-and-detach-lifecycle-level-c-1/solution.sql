CREATE TABLE IF NOT EXISTS events.partition_retention_log (
    partition_name text PRIMARY KEY,
    detached_at timestamptz NOT NULL DEFAULT now()
);
CREATE OR REPLACE FUNCTION events.detach_old_event_partition(partition_name text)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    EXECUTE format('ALTER TABLE events.event_log_partitioned DETACH PARTITION %I', partition_name);
    INSERT INTO events.partition_retention_log (partition_name)
    VALUES (partition_name)
    ON CONFLICT (partition_name) DO NOTHING;
END;
$$;
EXPLAIN
SELECT count(*)
FROM events.event_log_partitioned
WHERE event_time >= '2026-01-01'::timestamptz
  AND event_time < '2026-02-01'::timestamptz;

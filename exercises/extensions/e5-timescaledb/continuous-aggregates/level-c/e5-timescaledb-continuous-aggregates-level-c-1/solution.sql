CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE TABLE IF NOT EXISTS events.event_log_timescale (
  event_id bigint,
  occurred_at timestamptz NOT NULL,
  account_id bigint NOT NULL,
  event_type text NOT NULL
);
SELECT create_hypertable('events.event_log_timescale', by_range('occurred_at'), if_not_exists => TRUE);
CREATE MATERIALIZED VIEW IF NOT EXISTS events.event_counts_hourly
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', occurred_at) AS bucket, event_type, count(*) AS events
FROM events.event_log_timescale
GROUP BY bucket, event_type;
SELECT bucket, event_type, events
FROM events.event_counts_hourly
ORDER BY bucket DESC, event_type
LIMIT 20;
-- Critical drill: convert a phase-09 partitioned events table's analysis workload into a hypertable + continuous aggregate; compare query times.

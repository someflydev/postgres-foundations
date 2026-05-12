CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE TABLE IF NOT EXISTS events.event_log_timescale (
  event_id bigint,
  occurred_at timestamptz NOT NULL,
  account_id bigint NOT NULL,
  event_type text NOT NULL
);
SELECT create_hypertable(
  'events.event_log_timescale',
  by_range('occurred_at', INTERVAL '1 day'),
  if_not_exists => TRUE
);

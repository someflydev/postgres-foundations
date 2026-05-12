SELECT add_retention_policy('events.event_log_timescale', INTERVAL '180 days', if_not_exists => TRUE);
SELECT hypertable_name, drop_after
FROM timescaledb_information.jobs
WHERE proc_name = 'policy_retention';

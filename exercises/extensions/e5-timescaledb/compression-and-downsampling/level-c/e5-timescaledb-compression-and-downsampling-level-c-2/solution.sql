ALTER TABLE events.event_log_timescale
SET (timescaledb.compress, timescaledb.compress_segmentby = 'account_id');
SELECT add_compression_policy('events.event_log_timescale', INTERVAL '30 days', if_not_exists => TRUE);

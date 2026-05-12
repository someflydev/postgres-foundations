CREATE INDEX IF NOT EXISTS events_event_time_brin
    ON observability.events USING brin (event_time);
CREATE INDEX IF NOT EXISTS events_service_time_idx
    ON observability.events (service_name, event_time DESC);
CREATE INDEX IF NOT EXISTS events_trace_time_idx
    ON observability.events (trace_id, event_time);
CREATE INDEX IF NOT EXISTS events_error_service_idx
    ON observability.events (service_name, event_time DESC)
    WHERE severity IN ('warn', 'error');

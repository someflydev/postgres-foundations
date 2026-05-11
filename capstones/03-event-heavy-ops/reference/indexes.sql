CREATE INDEX device_events_2026_01_event_time_brin
    ON device_events_2026_01 USING brin (event_time);
CREATE INDEX device_events_2026_02_event_time_brin
    ON device_events_2026_02 USING brin (event_time);
CREATE INDEX device_events_2026_03_event_time_brin
    ON device_events_2026_03 USING brin (event_time);

CREATE INDEX device_events_2026_01_device_id_idx ON device_events_2026_01 (device_id);
CREATE INDEX device_events_2026_02_device_id_idx ON device_events_2026_02 (device_id);
CREATE INDEX device_events_2026_03_device_id_idx ON device_events_2026_03 (device_id);

CREATE INDEX device_events_2026_01_anomaly_idx
    ON device_events_2026_01 (device_id, event_time DESC)
    WHERE severity IN ('anomaly', 'critical');
CREATE INDEX device_events_2026_02_anomaly_idx
    ON device_events_2026_02 (device_id, event_time DESC)
    WHERE severity IN ('anomaly', 'critical');
CREATE INDEX device_events_2026_03_anomaly_idx
    ON device_events_2026_03 (device_id, event_time DESC)
    WHERE severity IN ('anomaly', 'critical');

CREATE INDEX devices_fleet_id_idx ON devices (fleet_id);
CREATE INDEX anomaly_notes_device_time_idx ON anomaly_notes (device_id, event_time DESC);

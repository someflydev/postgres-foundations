SELECT event_id, event_time, severity, event_type, reading
FROM device_events
WHERE device_id = 1001
  AND event_time >= timestamp with time zone '2026-03-10 00:00+00'
  AND event_time < timestamp with time zone '2026-03-11 00:00+00'
ORDER BY event_time DESC
LIMIT 200;

SELECT event_id, event_time, severity, event_type, payload
FROM device_events
WHERE device_id = 1001
  AND severity IN ('anomaly', 'critical')
  AND event_time >= timestamp with time zone '2026-03-04 00:00+00'
  AND event_time < timestamp with time zone '2026-03-11 00:00+00'
ORDER BY event_time;

SELECT device_id, count(*) AS anomaly_count
FROM device_events
WHERE severity IN ('anomaly', 'critical')
  AND event_time >= timestamp with time zone '2026-03-10 00:00+00'
  AND event_time < timestamp with time zone '2026-03-11 00:00+00'
GROUP BY device_id
ORDER BY anomaly_count DESC, device_id
LIMIT 25;

SELECT e.event_time, d.device_key, d.firmware_version, e.severity, e.event_type, e.reading
FROM device_events e
JOIN devices d ON d.id = e.device_id
WHERE e.device_id = 1001
  AND e.event_time >= timestamp with time zone '2026-03-04 00:00+00'
  AND e.event_time < timestamp with time zone '2026-03-11 00:00+00'
ORDER BY e.event_time;

SELECT severity, event_type, count(*) AS events_seen
FROM device_events
WHERE event_time >= timestamp with time zone '2026-03-10 00:00+00'
  AND event_time < timestamp with time zone '2026-03-11 00:00+00'
GROUP BY severity, event_type
ORDER BY events_seen DESC;

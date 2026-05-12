SELECT event_id, event_time, severity
FROM observability.events
WHERE service_name = 'checkout'
  AND event_time >= now() - interval '15 minutes'
ORDER BY event_time DESC
LIMIT 100;

SELECT service_name,
       percentile_cont(0.95) WITHIN GROUP (ORDER BY latency_ms) AS p95_latency_ms
FROM observability.events
WHERE event_time >= now() - interval '1 hour'
  AND latency_ms IS NOT NULL
GROUP BY service_name
ORDER BY service_name;

SELECT service_name, event_time, severity, attributes
FROM observability.events
WHERE trace_id = '00000000-0000-0000-0000-000000000001'
ORDER BY event_time;

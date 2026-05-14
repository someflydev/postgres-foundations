-- PostGIS profile required. Start from the service-zone containment or distance workload.
EXPLAIN (ANALYZE, BUFFERS)
SELECT e.id, e.event_name, z.zone_code
FROM logistics.delivery_events AS e
JOIN logistics.service_zones AS z
  ON ST_Contains(z.geom, e.geom)
WHERE z.zone_code = 'chi-loop';

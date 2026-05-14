-- Requires the PostGIS profile and the logistics_geo seed pack.
CREATE INDEX IF NOT EXISTS service_zones_geom_gist_idx
ON logistics.service_zones USING gist (geom);

CREATE INDEX IF NOT EXISTS delivery_events_geom_gist_idx
ON logistics.delivery_events USING gist (geom);

CREATE INDEX IF NOT EXISTS delivery_events_geog_gist_idx
ON logistics.delivery_events USING gist (geog);

ANALYZE logistics.service_zones;
ANALYZE logistics.delivery_events;

EXPLAIN (ANALYZE, BUFFERS)
SELECT e.id, e.event_name, z.zone_code
FROM logistics.delivery_events AS e
JOIN logistics.service_zones AS z
  ON ST_Contains(z.geom, e.geom)
WHERE z.zone_code = 'chi-loop';

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, event_name
FROM logistics.delivery_events
WHERE ST_DWithin(
    geog,
    ST_SetSRID(ST_MakePoint(-87.6298, 41.8781), 4326)::geography,
    5000
);

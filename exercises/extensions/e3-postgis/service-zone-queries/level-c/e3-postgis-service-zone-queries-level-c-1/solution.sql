CREATE INDEX IF NOT EXISTS service_zones_geom_gist_idx
    ON logistics.service_zones USING gist (geom);
CREATE INDEX IF NOT EXISTS delivery_events_geom_gist_idx
    ON logistics.delivery_events USING gist (geom);

SELECT z.zone_name, date_trunc('hour', e.occurred_at) AS hour, count(*) AS event_count
FROM logistics.service_zones AS z
JOIN logistics.delivery_events AS e
  ON ST_Contains(z.geom, e.geom)
GROUP BY z.zone_name, hour
ORDER BY hour, z.zone_name;

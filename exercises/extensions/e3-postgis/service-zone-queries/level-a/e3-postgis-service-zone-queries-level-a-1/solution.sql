SELECT z.zone_name, date_trunc('hour', e.occurred_at) AS hour, count(*) AS events
FROM logistics.service_zones AS z
JOIN logistics.delivery_events AS e
  ON ST_Contains(z.geom, e.geom)
GROUP BY z.zone_name, hour
ORDER BY hour, z.zone_name;

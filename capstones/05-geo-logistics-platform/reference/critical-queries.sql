SELECT c.courier_id, c.display_name
FROM logistics.couriers c
JOIN logistics.service_zones z ON z.region_id = c.region_id
WHERE z.active
  AND c.status = 'available'
  AND ST_Contains(z.boundary, c.current_location)
ORDER BY c.last_seen_at DESC
LIMIT 10;

SELECT zone_id, date_trunc('day', requested_at) AS service_day,
       count(*) AS deliveries,
       count(*) FILTER (WHERE delivered_at <= promised_at) AS on_time
FROM logistics.deliveries
GROUP BY zone_id, date_trunc('day', requested_at)
ORDER BY service_day DESC, zone_id;

SELECT breadcrumb_id, recorded_at, ST_AsText(location) AS location
FROM logistics.courier_breadcrumbs
WHERE courier_id = 1
  AND recorded_at >= timestamp with time zone '2026-05-01 00:00+00'
  AND recorded_at < timestamp with time zone '2026-05-02 00:00+00'
ORDER BY recorded_at;

SELECT delivery_id, ts_rank(note_tsv, plainto_tsquery('english', 'gate code')) AS rank
FROM logistics.deliveries
WHERE note_tsv @@ plainto_tsquery('english', 'gate code')
ORDER BY rank DESC, requested_at DESC
LIMIT 20;

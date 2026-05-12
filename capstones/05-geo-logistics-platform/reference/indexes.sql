CREATE INDEX IF NOT EXISTS couriers_region_status_seen_idx
    ON logistics.couriers (region_id, status, last_seen_at DESC);
CREATE INDEX IF NOT EXISTS couriers_current_location_gix
    ON logistics.couriers USING gist (current_location);
CREATE INDEX IF NOT EXISTS service_zones_boundary_gix
    ON logistics.service_zones USING gist (boundary);
CREATE INDEX IF NOT EXISTS deliveries_zone_requested_idx
    ON logistics.deliveries (zone_id, requested_at DESC);
CREATE INDEX IF NOT EXISTS deliveries_note_tsv_gin
    ON logistics.deliveries USING gin (note_tsv);
CREATE INDEX IF NOT EXISTS courier_breadcrumbs_location_gix
    ON logistics.courier_breadcrumbs USING gist (location);
CREATE INDEX IF NOT EXISTS courier_breadcrumbs_courier_time_idx
    ON logistics.courier_breadcrumbs (courier_id, recorded_at DESC);

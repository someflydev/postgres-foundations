CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_partman;

CREATE SCHEMA IF NOT EXISTS logistics;

CREATE TABLE logistics.couriers (
    courier_id bigserial PRIMARY KEY,
    region_id text NOT NULL,
    display_name text NOT NULL,
    status text NOT NULL CHECK (status IN ('available', 'assigned', 'offline')),
    last_seen_at timestamptz NOT NULL DEFAULT now(),
    current_location geometry(Point, 4326) NOT NULL
);

CREATE TABLE logistics.vehicles (
    vehicle_id bigserial PRIMARY KEY,
    courier_id bigint NOT NULL REFERENCES logistics.couriers(courier_id),
    plate text NOT NULL UNIQUE,
    capacity_kg numeric(8,2) NOT NULL CHECK (capacity_kg > 0)
);

CREATE TABLE logistics.service_zones (
    zone_id bigserial PRIMARY KEY,
    region_id text NOT NULL,
    zone_name text NOT NULL,
    boundary geometry(Polygon, 4326) NOT NULL,
    active boolean NOT NULL DEFAULT true
);

CREATE TABLE logistics.deliveries (
    delivery_id bigserial PRIMARY KEY,
    region_id text NOT NULL,
    zone_id bigint NOT NULL REFERENCES logistics.service_zones(zone_id),
    courier_id bigint REFERENCES logistics.couriers(courier_id),
    requested_at timestamptz NOT NULL,
    promised_at timestamptz NOT NULL,
    delivered_at timestamptz,
    status text NOT NULL CHECK (status IN ('requested', 'assigned', 'delivered', 'failed')),
    note text NOT NULL DEFAULT '',
    note_tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', note)) STORED
);

CREATE TABLE logistics.courier_breadcrumbs (
    breadcrumb_id bigserial,
    courier_id bigint NOT NULL REFERENCES logistics.couriers(courier_id),
    recorded_at timestamptz NOT NULL,
    location geometry(Point, 4326) NOT NULL,
    speed_mps numeric(8,2),
    PRIMARY KEY (breadcrumb_id, recorded_at)
) PARTITION BY RANGE (recorded_at);

CREATE TABLE logistics.courier_breadcrumbs_2026_05
PARTITION OF logistics.courier_breadcrumbs
FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');

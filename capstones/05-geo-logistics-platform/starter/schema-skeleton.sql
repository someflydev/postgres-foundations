CREATE SCHEMA IF NOT EXISTS logistics;

CREATE TABLE logistics.couriers (
    courier_id bigserial PRIMARY KEY,
    region_id text NOT NULL,
    display_name text NOT NULL
);

CREATE TABLE logistics.deliveries (
    delivery_id bigserial PRIMARY KEY,
    region_id text NOT NULL,
    courier_id bigint REFERENCES logistics.couriers(courier_id),
    requested_at timestamptz NOT NULL DEFAULT now()
);

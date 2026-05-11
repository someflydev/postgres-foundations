CREATE TABLE device_fleets (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_id uuid NOT NULL,
    name text NOT NULL
);

CREATE TABLE devices (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fleet_id bigint NOT NULL,
    device_key text NOT NULL UNIQUE
);

-- Add a partitioned device_events table keyed by event_time.

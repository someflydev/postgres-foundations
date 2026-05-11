CREATE TABLE device_fleets (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_id uuid NOT NULL,
    name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (account_id, name)
);

CREATE TABLE devices (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fleet_id bigint NOT NULL REFERENCES device_fleets(id),
    device_key text NOT NULL UNIQUE,
    firmware_version text NOT NULL,
    installed_at timestamptz NOT NULL DEFAULT now(),
    retired_at timestamptz
);

CREATE TABLE device_events (
    event_id bigint GENERATED ALWAYS AS IDENTITY,
    device_id bigint NOT NULL REFERENCES devices(id),
    event_time timestamptz NOT NULL,
    received_at timestamptz NOT NULL DEFAULT now(),
    severity text NOT NULL CHECK (severity IN ('info', 'warning', 'anomaly', 'critical')),
    event_type text NOT NULL,
    reading numeric(12, 4),
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    PRIMARY KEY (event_time, event_id)
) PARTITION BY RANGE (event_time);

CREATE TABLE device_events_2026_01 PARTITION OF device_events
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

CREATE TABLE device_events_2026_02 PARTITION OF device_events
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

CREATE TABLE device_events_2026_03 PARTITION OF device_events
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');

CREATE TABLE anomaly_notes (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    device_id bigint NOT NULL REFERENCES devices(id),
    event_time timestamptz NOT NULL,
    note text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

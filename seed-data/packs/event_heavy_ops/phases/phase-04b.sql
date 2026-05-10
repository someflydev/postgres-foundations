-- domain: event_heavy_ops
-- phase: 04b
-- depends: phase-02
-- description: range-indexed event windows for append-heavy operations

CREATE SCHEMA IF NOT EXISTS events;

CREATE TABLE IF NOT EXISTS events.event_windows (
    id bigint generated always as identity PRIMARY KEY,
    source_id bigint NOT NULL REFERENCES events.sources(id),
    "window" tstzrange NOT NULL,
    label text NOT NULL DEFAULT 'ingest window',
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_id, "window"),
    CONSTRAINT event_windows_nonempty_check CHECK (NOT isempty("window"))
);

CREATE INDEX IF NOT EXISTS event_windows_window_gist
    ON events.event_windows USING gist ("window");

INSERT INTO events.event_windows (source_id, "window", label)
VALUES
    (
        (SELECT id FROM events.sources WHERE source_key = 'checkout-prod'),
        tstzrange('2026-03-01 12:00:00+00', '2026-03-01 12:05:00+00', '[)'),
        'checkout burst'
    ),
    (
        (SELECT id FROM events.sources WHERE source_key = 'billing-prod'),
        tstzrange('2026-03-01 12:01:00+00', '2026-03-01 12:06:00+00', '[)'),
        'billing capture'
    )
ON CONFLICT DO NOTHING;

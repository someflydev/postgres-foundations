CREATE SCHEMA IF NOT EXISTS cold_archive;

CREATE TABLE IF NOT EXISTS cold_archive.device_events_export_log (
    partition_name text PRIMARY KEY,
    detached_at timestamptz NOT NULL DEFAULT now(),
    archive_uri text NOT NULL
);

ALTER TABLE device_events DETACH PARTITION device_events_2026_01;

INSERT INTO cold_archive.device_events_export_log (partition_name, archive_uri)
VALUES ('device_events_2026_01', 's3://example-cold-archive/device-events/2026/01/')
ON CONFLICT (partition_name) DO UPDATE
SET detached_at = excluded.detached_at,
    archive_uri = excluded.archive_uri;

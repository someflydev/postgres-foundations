-- Exclusion constraints over overlapping ranges are not a plain CHECK
-- constraint; PostgreSQL enforces them through an index-backed access method,
-- commonly GiST for range overlap operators. For the read workload, verify the
-- same operator family directly with an indexed range query.
DROP INDEX IF EXISTS appointments_window_gist_idx;

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, provider_id, starts_at, ends_at
FROM scheduling.appointments
WHERE tstzrange(starts_at, ends_at, '[)') && tstzrange('2025-02-03 09:00:00+00', '2025-02-03 12:00:00+00', '[)');

CREATE INDEX appointments_window_gist_idx
ON scheduling.appointments USING gist (tstzrange(starts_at, ends_at, '[)'));
ANALYZE scheduling.appointments;

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, provider_id, starts_at, ends_at
FROM scheduling.appointments
WHERE tstzrange(starts_at, ends_at, '[)') && tstzrange('2025-02-03 09:00:00+00', '2025-02-03 12:00:00+00', '[)');

DROP INDEX IF EXISTS scheduling.appointments_provider_start_status_phase7a_idx;
CREATE INDEX appointments_provider_start_status_phase7a_idx
ON scheduling.appointments (provider_id, starts_at, status);
ANALYZE scheduling.appointments;

SELECT id, starts_at, ends_at, status
FROM scheduling.appointments
WHERE provider_id = 1
  AND starts_at >= '2026-01-01'::timestamptz
ORDER BY starts_at
LIMIT 30;

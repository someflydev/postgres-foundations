DELETE FROM scheduling.appointments WHERE starts_at = '2026-02-12 19:00:00+00' RETURNING starts_at, status;

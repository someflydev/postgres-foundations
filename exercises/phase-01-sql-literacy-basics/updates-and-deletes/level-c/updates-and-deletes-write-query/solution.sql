UPDATE scheduling.appointments SET status = 'completed' WHERE starts_at = '2026-02-10 15:00:00+00' RETURNING starts_at, ends_at, status;

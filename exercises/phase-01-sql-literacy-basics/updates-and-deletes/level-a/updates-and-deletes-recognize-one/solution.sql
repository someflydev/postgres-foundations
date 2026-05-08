UPDATE scheduling.appointments SET status = 'confirmed' WHERE starts_at = '2026-02-10 15:00:00+00' RETURNING starts_at, status;

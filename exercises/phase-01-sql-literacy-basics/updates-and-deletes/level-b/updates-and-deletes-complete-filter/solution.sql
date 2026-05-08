UPDATE scheduling.appointments SET status = 'checked_in' WHERE starts_at = '2026-02-11 17:00:00+00' RETURNING starts_at, status;

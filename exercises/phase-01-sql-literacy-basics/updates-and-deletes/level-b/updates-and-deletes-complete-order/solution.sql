DELETE FROM scheduling.appointments WHERE status = 'cancelled' RETURNING starts_at, status;

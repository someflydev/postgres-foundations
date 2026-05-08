DELETE FROM scheduling.appointments WHERE /* protective predicate */ RETURNING starts_at, status;

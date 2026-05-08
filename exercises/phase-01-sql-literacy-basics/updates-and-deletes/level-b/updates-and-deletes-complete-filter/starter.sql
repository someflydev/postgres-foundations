UPDATE scheduling.appointments SET status = /* new status */ WHERE /* exact row predicate */ RETURNING starts_at, status;

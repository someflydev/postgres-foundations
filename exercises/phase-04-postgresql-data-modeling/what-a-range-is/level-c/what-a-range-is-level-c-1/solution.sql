SELECT lower(tstzrange(starts_at, ends_at, '[)')) FROM scheduling.appointments ORDER BY starts_at;

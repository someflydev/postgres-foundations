SELECT tstzrange(starts_at, ends_at, '[)') AS slot FROM scheduling.appointments ORDER BY starts_at;

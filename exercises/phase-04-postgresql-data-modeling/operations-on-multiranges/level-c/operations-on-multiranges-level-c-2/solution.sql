SELECT display_name, working_hours - tstzrange('2026-02-10 15:00+00', '2026-02-10 16:00+00', '[)') FROM scheduling.professionals ORDER BY display_name;

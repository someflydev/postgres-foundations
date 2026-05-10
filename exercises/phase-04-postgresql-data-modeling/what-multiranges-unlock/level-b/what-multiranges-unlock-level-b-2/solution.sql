SELECT display_name FROM scheduling.professionals WHERE working_hours @> '2026-02-10 15:00+00'::timestamptz ORDER BY display_name;

SELECT /* choose columns */ starts_at, status FROM scheduling.appointments WHERE starts_at BETWEEN '2026-02-10 00:00:00+00' AND '2026-02-10 23:59:59+00' ORDER BY starts_at;

SELECT a.id, a.starts_at, a.ends_at FROM scheduling.appointments a WHERE a.starts_at < a.ends_at ORDER BY a.id;

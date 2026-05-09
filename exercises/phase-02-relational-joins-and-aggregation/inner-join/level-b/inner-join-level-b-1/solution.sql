SELECT a.starts_at, p.display_name FROM scheduling.appointments a INNER JOIN scheduling.providers p ON p.id = a.provider_id ORDER BY a.starts_at;

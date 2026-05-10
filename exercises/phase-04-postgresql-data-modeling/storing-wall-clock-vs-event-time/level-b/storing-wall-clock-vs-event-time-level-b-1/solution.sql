SELECT p.display_name, p.timezone, a.starts_at AT TIME ZONE p.timezone AS local_start FROM scheduling.appointments a INNER JOIN scheduling.providers p ON p.id=a.provider_id ORDER BY a.starts_at;

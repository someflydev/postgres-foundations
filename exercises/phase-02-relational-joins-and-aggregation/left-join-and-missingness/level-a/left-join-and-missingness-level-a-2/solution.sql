SELECT p.display_name, a.status FROM scheduling.providers p LEFT JOIN scheduling.appointments a ON a.provider_id = p.id ORDER BY p.display_name, a.status;

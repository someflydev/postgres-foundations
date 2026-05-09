SELECT a.id, p.display_name, c.email FROM scheduling.appointments a INNER JOIN scheduling.providers p ON p.id = a.provider_id INNER JOIN scheduling.clients c ON c.id = a.client_id ORDER BY a.id;

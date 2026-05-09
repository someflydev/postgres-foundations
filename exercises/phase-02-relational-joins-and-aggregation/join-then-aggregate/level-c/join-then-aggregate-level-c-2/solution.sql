SELECT p.display_name, count(a.id) AS appointments FROM scheduling.providers p LEFT JOIN scheduling.appointments a ON a.provider_id = p.id GROUP BY p.display_name ORDER BY p.display_name;

SELECT provider_id, count(*) AS appointments FROM scheduling.appointments GROUP BY provider_id HAVING count(*) >= 2 ORDER BY provider_id;

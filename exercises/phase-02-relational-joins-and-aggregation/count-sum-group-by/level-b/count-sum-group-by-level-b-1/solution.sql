SELECT status, count(*) AS appointments FROM scheduling.appointments GROUP BY status ORDER BY status;

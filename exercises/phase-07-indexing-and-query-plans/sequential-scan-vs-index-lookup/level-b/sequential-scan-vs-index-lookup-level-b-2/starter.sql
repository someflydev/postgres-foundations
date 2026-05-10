-- Compare this broad query with the selective query from this lesson.
SELECT status, count(*)
FROM ecommerce.orders
GROUP BY status
ORDER BY status;

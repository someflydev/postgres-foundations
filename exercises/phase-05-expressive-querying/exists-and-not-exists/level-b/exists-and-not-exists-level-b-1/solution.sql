SELECT c.email
FROM ecommerce.customers c
WHERE EXISTS (
    SELECT 1
    FROM ecommerce.orders o
    WHERE o.customer_id = c.id
      AND o.status = 'paid'
)
AND NOT EXISTS (
    SELECT 1
    FROM ecommerce.customer_segments s
    WHERE s.customer_id = c.id
      AND s.segment IS NULL
)
ORDER BY c.email
LIMIT 25;

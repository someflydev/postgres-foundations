SELECT c.email, count(DISTINCT o.id) AS orders FROM ecommerce.customers c LEFT JOIN ecommerce.orders o ON o.customer_id = c.id GROUP BY c.email HAVING count(DISTINCT o.id) >= 1 ORDER BY c.email;

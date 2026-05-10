SELECT c.email, top_orders.order_number, top_orders.total_amount
FROM ecommerce.customers c
CROSS JOIN LATERAL (
    SELECT o.order_number, o.total_amount
    FROM ecommerce.orders o
    WHERE o.customer_id = c.id
    ORDER BY o.total_amount DESC, o.id
    LIMIT 3
) AS top_orders
ORDER BY c.email, top_orders.total_amount DESC, top_orders.order_number
LIMIT 60;

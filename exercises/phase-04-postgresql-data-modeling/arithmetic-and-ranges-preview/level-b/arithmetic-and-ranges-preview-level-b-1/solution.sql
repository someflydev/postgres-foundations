SELECT order_number, ordered_at + interval '2 days' AS followup_at FROM ecommerce.orders ORDER BY order_number;

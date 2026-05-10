SELECT order_number FROM ecommerce.orders WHERE ordered_at >= '2026-01-05'::timestamptz AND ordered_at < '2026-01-07'::timestamptz ORDER BY order_number;

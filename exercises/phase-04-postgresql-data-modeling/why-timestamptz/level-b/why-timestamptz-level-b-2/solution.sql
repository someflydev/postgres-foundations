SELECT order_number, ordered_at FROM ecommerce.orders WHERE ordered_at >= '2026-01-06 00:00:00+00'::timestamptz ORDER BY ordered_at;

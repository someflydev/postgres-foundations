SELECT order_number, ordered_at, ordered_at - '2026-01-05 00:00:00+00'::timestamptz AS age_from_anchor FROM ecommerce.orders ORDER BY order_number;

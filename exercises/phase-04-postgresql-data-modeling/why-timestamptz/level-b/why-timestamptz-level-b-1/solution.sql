SELECT order_number, ordered_at AT TIME ZONE 'America/Chicago' AS ordered_at_chicago FROM ecommerce.orders ORDER BY ordered_at;

SELECT order_number FROM ecommerce.orders WHERE metadata ->> 'channel' = 'web' ORDER BY order_number;

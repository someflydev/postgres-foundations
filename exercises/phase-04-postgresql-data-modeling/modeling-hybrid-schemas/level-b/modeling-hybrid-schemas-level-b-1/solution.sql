SELECT order_number, status, metadata ->> 'campaign' AS campaign FROM ecommerce.orders ORDER BY order_number;

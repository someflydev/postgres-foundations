SELECT order_number, metadata ->> 'channel' AS channel FROM ecommerce.orders ORDER BY order_number;

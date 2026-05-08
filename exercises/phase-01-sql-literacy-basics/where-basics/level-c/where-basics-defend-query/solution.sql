SELECT order_number, status FROM ecommerce.orders WHERE status = 'placed' OR status = 'paid' ORDER BY order_number;

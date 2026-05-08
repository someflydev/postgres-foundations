SELECT order_number, total_amount FROM ecommerce.orders WHERE status IN ('paid', 'placed') ORDER BY total_amount;

SELECT order_number, metadata -> 'shippping' AS misspelled_shipping FROM ecommerce.orders WHERE metadata ? 'shippping' ORDER BY order_number;

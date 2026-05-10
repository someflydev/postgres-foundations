SELECT order_number, metadata -> 'warehouse' AS cold_fulfillment_detail FROM ecommerce.orders WHERE metadata ? 'warehouse' ORDER BY order_number;

INSERT INTO ecommerce.products (sku, name, price, stock_on_hand) VALUES ('HAT-PG-001', 'Postgres Hat', 22.00, 15), ('CARD-PG-002', 'Postgres Greeting Card', 3.00, 50) RETURNING sku, price;

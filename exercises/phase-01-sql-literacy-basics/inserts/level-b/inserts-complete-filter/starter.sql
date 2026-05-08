INSERT INTO ecommerce.products (sku, name, price, stock_on_hand) VALUES (/* sku */, /* name */, /* price */, /* stock */) RETURNING sku, name, stock_on_hand;

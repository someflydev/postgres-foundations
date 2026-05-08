SELECT /* choose columns */ sku, name, stock_on_hand FROM ecommerce.products WHERE stock_on_hand >= 25 ORDER BY sku;

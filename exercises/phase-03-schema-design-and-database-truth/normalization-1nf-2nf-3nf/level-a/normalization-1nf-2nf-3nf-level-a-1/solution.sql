DROP TABLE IF EXISTS ecommerce.normalization_1nf_2nf_3nf_a_1_items;
DROP TABLE IF EXISTS ecommerce.normalization_1nf_2nf_3nf_a_1_orders;
DROP TABLE IF EXISTS ecommerce.normalization_1nf_2nf_3nf_a_1_customers;
CREATE TABLE ecommerce.normalization_1nf_2nf_3nf_a_1_customers (
    id bigint generated always as identity PRIMARY KEY,
    email text NOT NULL UNIQUE,
    full_name text NOT NULL
);

CREATE TABLE ecommerce.normalization_1nf_2nf_3nf_a_1_orders (
    id bigint generated always as identity PRIMARY KEY,
    order_number text NOT NULL UNIQUE,
    customer_id bigint NOT NULL REFERENCES ecommerce.normalization_1nf_2nf_3nf_a_1_customers(id)
);

CREATE TABLE ecommerce.normalization_1nf_2nf_3nf_a_1_items (
    id bigint generated always as identity PRIMARY KEY,
    order_id bigint NOT NULL REFERENCES ecommerce.normalization_1nf_2nf_3nf_a_1_orders(id),
    sku text NOT NULL,
    quantity integer NOT NULL,
    CONSTRAINT normalization_1nf_2nf_3nf_a_1_items_quantity_positive CHECK (quantity > 0),
    CONSTRAINT normalization_1nf_2nf_3nf_a_1_items_order_sku_unique UNIQUE (order_id, sku)
);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'ecommerce'
  AND table_name = 'normalization_1nf_2nf_3nf_a_1_items'
ORDER BY table_name;

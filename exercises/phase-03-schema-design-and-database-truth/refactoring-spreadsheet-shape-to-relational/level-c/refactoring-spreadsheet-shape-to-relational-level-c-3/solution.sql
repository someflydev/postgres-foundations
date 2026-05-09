DROP TABLE IF EXISTS ecommerce.refactoring_spreadsheet_shape_to_relational_c_3_items;
DROP TABLE IF EXISTS ecommerce.refactoring_spreadsheet_shape_to_relational_c_3_orders;
DROP TABLE IF EXISTS ecommerce.refactoring_spreadsheet_shape_to_relational_c_3_products;
DROP TABLE IF EXISTS ecommerce.refactoring_spreadsheet_shape_to_relational_c_3_customers;
CREATE TABLE ecommerce.refactoring_spreadsheet_shape_to_relational_c_3_customers (
    id bigint generated always as identity PRIMARY KEY,
    email text NOT NULL UNIQUE,
    full_name text NOT NULL,
    country_code text NOT NULL REFERENCES ecommerce.countries(code)
);

CREATE TABLE ecommerce.refactoring_spreadsheet_shape_to_relational_c_3_products (
    id bigint generated always as identity PRIMARY KEY,
    sku text NOT NULL UNIQUE,
    name text NOT NULL
);

CREATE TABLE ecommerce.refactoring_spreadsheet_shape_to_relational_c_3_orders (
    id bigint generated always as identity PRIMARY KEY,
    order_number text NOT NULL UNIQUE,
    customer_id bigint NOT NULL REFERENCES ecommerce.refactoring_spreadsheet_shape_to_relational_c_3_customers(id),
    order_date date NOT NULL,
    currency text NOT NULL REFERENCES ecommerce.currencies(code)
);

CREATE TABLE ecommerce.refactoring_spreadsheet_shape_to_relational_c_3_items (
    id bigint generated always as identity PRIMARY KEY,
    order_id bigint NOT NULL REFERENCES ecommerce.refactoring_spreadsheet_shape_to_relational_c_3_orders(id),
    product_id bigint NOT NULL REFERENCES ecommerce.refactoring_spreadsheet_shape_to_relational_c_3_products(id),
    quantity integer NOT NULL CHECK (quantity > 0),
    unit_price numeric(12,2) NOT NULL CHECK (unit_price >= 0),
    UNIQUE (order_id, product_id)
);

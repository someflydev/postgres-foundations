# Solution

The legacy file `seed-data/packs/ecommerce/fixtures/spreadsheet-legacy.csv` mixes order facts, customer facts, product facts, and line-item facts. Without this constraint, an incident could occur when `ada@example.com` appears as both `Ada Lovelace` and `Ada L.`, or when `BK-SQL-001` carries conflicting prices and reporting treats both as authoritative.

A concrete relational target is:

```sql
CREATE TABLE ecommerce.legacy_customers (
    id bigint generated always as identity PRIMARY KEY,
    email text NOT NULL UNIQUE,
    full_name text NOT NULL,
    country_code text NOT NULL REFERENCES ecommerce.countries(code)
);

CREATE TABLE ecommerce.legacy_products (
    id bigint generated always as identity PRIMARY KEY,
    sku text NOT NULL UNIQUE,
    name text NOT NULL
);

CREATE TABLE ecommerce.legacy_orders (
    id bigint generated always as identity PRIMARY KEY,
    order_number text NOT NULL UNIQUE,
    customer_id bigint NOT NULL REFERENCES ecommerce.legacy_customers(id),
    order_date date NOT NULL,
    currency text NOT NULL REFERENCES ecommerce.currencies(code)
);

CREATE TABLE ecommerce.legacy_order_items (
    id bigint generated always as identity PRIMARY KEY,
    order_id bigint NOT NULL REFERENCES ecommerce.legacy_orders(id),
    product_id bigint NOT NULL REFERENCES ecommerce.legacy_products(id),
    quantity integer NOT NULL CHECK (quantity > 0),
    unit_price numeric(12,2) NOT NULL CHECK (unit_price >= 0),
    UNIQUE (order_id, product_id)
);
```

Before enforcing the constraints, quarantine rows with zero or negative quantity, unknown countries such as `GB` if the reference table lacks it, and conflicting product/customer names. The migration should preserve the raw import for audit while loading cleaned facts into the normalized tables.

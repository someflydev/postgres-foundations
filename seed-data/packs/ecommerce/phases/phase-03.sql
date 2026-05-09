-- domain: ecommerce
-- phase: 03
-- depends: phase-02
-- description: constraints and reference tables for database-enforced truth

CREATE SCHEMA IF NOT EXISTS ecommerce;

CREATE TABLE IF NOT EXISTS ecommerce.countries (
    code text PRIMARY KEY,
    name text NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS ecommerce.currencies (
    code text PRIMARY KEY,
    name text NOT NULL UNIQUE,
    minor_unit integer NOT NULL DEFAULT 2,
    CONSTRAINT currencies_minor_unit_check CHECK (minor_unit >= 0)
);

INSERT INTO ecommerce.countries (code, name)
VALUES
    ('US', 'United States'),
    ('CA', 'Canada')
ON CONFLICT (code) DO NOTHING;

INSERT INTO ecommerce.currencies (code, name, minor_unit)
VALUES
    ('USD', 'US Dollar', 2),
    ('CAD', 'Canadian Dollar', 2)
ON CONFLICT (code) DO NOTHING;

-- In phase 2, customer country was not modeled. In phase 3 we add a
-- reference-backed country code, backfill existing customers, then make it
-- required so every future customer carries the same fact shape.
ALTER TABLE ecommerce.customers
    ADD COLUMN IF NOT EXISTS country_code text;

UPDATE ecommerce.customers
SET country_code = 'US'
WHERE country_code IS NULL;

ALTER TABLE ecommerce.customers
    ALTER COLUMN email SET NOT NULL,
    ALTER COLUMN full_name SET NOT NULL,
    ALTER COLUMN country_code SET DEFAULT 'US',
    ALTER COLUMN country_code SET NOT NULL;

ALTER TABLE ecommerce.products
    ALTER COLUMN sku SET NOT NULL,
    ALTER COLUMN name SET NOT NULL,
    ALTER COLUMN currency SET NOT NULL;

ALTER TABLE ecommerce.orders
    ALTER COLUMN customer_id SET NOT NULL,
    ALTER COLUMN order_number SET NOT NULL,
    ALTER COLUMN total_amount SET NOT NULL,
    ALTER COLUMN currency SET NOT NULL;

ALTER TABLE ecommerce.order_items
    ALTER COLUMN order_id SET NOT NULL,
    ALTER COLUMN product_id SET NOT NULL,
    ALTER COLUMN quantity SET NOT NULL,
    ALTER COLUMN unit_price SET NOT NULL,
    ALTER COLUMN currency SET NOT NULL;

DO $$
BEGIN
    ALTER TABLE ecommerce.customers
        ADD CONSTRAINT customers_email_unique UNIQUE (email);
EXCEPTION
    WHEN duplicate_table OR duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE ecommerce.products
        ADD CONSTRAINT products_sku_unique UNIQUE (sku);
EXCEPTION
    WHEN duplicate_table OR duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE ecommerce.orders
        ADD CONSTRAINT orders_total_amount_nonnegative CHECK (total_amount >= 0);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE ecommerce.order_items
        ADD CONSTRAINT order_items_quantity_positive CHECK (quantity > 0);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE ecommerce.customers
        ADD CONSTRAINT customers_country_code_fkey
        FOREIGN KEY (country_code) REFERENCES ecommerce.countries(code);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE ecommerce.products
        ADD CONSTRAINT products_currency_fkey
        FOREIGN KEY (currency) REFERENCES ecommerce.currencies(code);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE ecommerce.orders
        ADD CONSTRAINT orders_currency_fkey
        FOREIGN KEY (currency) REFERENCES ecommerce.currencies(code);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;

DO $$
BEGIN
    ALTER TABLE ecommerce.order_items
        ADD CONSTRAINT order_items_currency_fkey
        FOREIGN KEY (currency) REFERENCES ecommerce.currencies(code);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END
$$;

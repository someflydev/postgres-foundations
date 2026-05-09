DROP TABLE IF EXISTS ecommerce.defaults_and_generated_columns_b_5;
CREATE TABLE ecommerce.defaults_and_generated_columns_b_5 (
    id bigint generated always as identity PRIMARY KEY,
    quantity integer NOT NULL DEFAULT 1,
    unit_price numeric(12,2) NOT NULL DEFAULT 0,
    line_total numeric(12,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE ecommerce.defaults_and_generated_columns_b_5
    ADD CONSTRAINT defaults_and_generated_columns_b_5_quantity_positive CHECK (quantity > 0);

ALTER TABLE ecommerce.defaults_and_generated_columns_b_5
    ADD CONSTRAINT defaults_and_generated_columns_b_5_unit_price_nonnegative CHECK (unit_price >= 0);

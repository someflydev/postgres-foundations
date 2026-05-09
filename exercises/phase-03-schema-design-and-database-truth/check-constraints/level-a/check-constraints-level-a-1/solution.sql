DROP TABLE IF EXISTS ecommerce.check_constraints_a_1;
CREATE TABLE ecommerce.check_constraints_a_1 (
    id bigint generated always as identity PRIMARY KEY,
    quantity integer,
    unit_price numeric(12,2),
    starts_at timestamptz,
    ends_at timestamptz
);

ALTER TABLE ecommerce.check_constraints_a_1
    ALTER COLUMN quantity SET NOT NULL,
    ALTER COLUMN unit_price SET NOT NULL;

ALTER TABLE ecommerce.check_constraints_a_1
    ADD CONSTRAINT check_constraints_a_1_quantity_positive CHECK (quantity > 0);

ALTER TABLE ecommerce.check_constraints_a_1
    ADD CONSTRAINT check_constraints_a_1_unit_price_nonnegative CHECK (unit_price >= 0);

ALTER TABLE ecommerce.check_constraints_a_1
    ADD CONSTRAINT check_constraints_a_1_starts_before_ends
    CHECK (starts_at IS NULL OR ends_at IS NULL OR starts_at < ends_at);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'ecommerce'
  AND table_name = 'check_constraints_a_1'
ORDER BY table_name;

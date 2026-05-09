DROP TABLE IF EXISTS ecommerce.check_constraints_c_6;
CREATE TABLE ecommerce.check_constraints_c_6 (
    id bigint generated always as identity PRIMARY KEY,
    quantity integer,
    unit_price numeric(12,2),
    starts_at timestamptz,
    ends_at timestamptz
);

ALTER TABLE ecommerce.check_constraints_c_6
    ALTER COLUMN quantity SET NOT NULL,
    ALTER COLUMN unit_price SET NOT NULL;

ALTER TABLE ecommerce.check_constraints_c_6
    ADD CONSTRAINT check_constraints_c_6_quantity_positive CHECK (quantity > 0);

ALTER TABLE ecommerce.check_constraints_c_6
    ADD CONSTRAINT check_constraints_c_6_unit_price_nonnegative CHECK (unit_price >= 0);

ALTER TABLE ecommerce.check_constraints_c_6
    ADD CONSTRAINT check_constraints_c_6_starts_before_ends
    CHECK (starts_at IS NULL OR ends_at IS NULL OR starts_at < ends_at);

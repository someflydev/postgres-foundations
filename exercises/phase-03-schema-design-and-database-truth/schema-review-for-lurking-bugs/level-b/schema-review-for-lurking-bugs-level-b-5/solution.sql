DROP TABLE IF EXISTS ecommerce.schema_review_for_lurking_bugs_b_5;
CREATE TABLE ecommerce.schema_review_for_lurking_bugs_b_5 (
    id bigint generated always as identity PRIMARY KEY,
    order_number text,
    quantity integer,
    status text,
    starts_at timestamptz,
    ends_at timestamptz
);

ALTER TABLE ecommerce.schema_review_for_lurking_bugs_b_5
    ALTER COLUMN order_number SET NOT NULL,
    ALTER COLUMN quantity SET NOT NULL,
    ALTER COLUMN status SET NOT NULL;

ALTER TABLE ecommerce.schema_review_for_lurking_bugs_b_5
    ADD CONSTRAINT schema_review_for_lurking_bugs_b_5_order_number_unique UNIQUE (order_number);

ALTER TABLE ecommerce.schema_review_for_lurking_bugs_b_5
    ADD CONSTRAINT schema_review_for_lurking_bugs_b_5_quantity_positive CHECK (quantity > 0);

ALTER TABLE ecommerce.schema_review_for_lurking_bugs_b_5
    ADD CONSTRAINT schema_review_for_lurking_bugs_b_5_status_known CHECK (status IN ('draft', 'paid', 'cancelled'));

ALTER TABLE ecommerce.schema_review_for_lurking_bugs_b_5
    ADD CONSTRAINT schema_review_for_lurking_bugs_b_5_time_order CHECK (starts_at IS NULL OR ends_at IS NULL OR starts_at < ends_at);

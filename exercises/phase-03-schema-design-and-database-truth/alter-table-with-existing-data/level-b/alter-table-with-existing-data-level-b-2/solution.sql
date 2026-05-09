DROP TABLE IF EXISTS ecommerce.alter_table_with_existing_data_b_2;
CREATE TABLE ecommerce.alter_table_with_existing_data_b_2 (
    id bigint generated always as identity PRIMARY KEY,
    email text,
    imported_at timestamptz,
    total_amount numeric(12,2)
);

UPDATE ecommerce.alter_table_with_existing_data_b_2
SET imported_at = now()
WHERE imported_at IS NULL;

ALTER TABLE ecommerce.alter_table_with_existing_data_b_2
    ALTER COLUMN email SET NOT NULL,
    ALTER COLUMN imported_at SET DEFAULT now(),
    ALTER COLUMN imported_at SET NOT NULL,
    ALTER COLUMN total_amount SET DEFAULT 0,
    ALTER COLUMN total_amount SET NOT NULL;

ALTER TABLE ecommerce.alter_table_with_existing_data_b_2
    ADD CONSTRAINT alter_table_with_existing_data_b_2_email_unique UNIQUE (email);

ALTER TABLE ecommerce.alter_table_with_existing_data_b_2
    ADD CONSTRAINT alter_table_with_existing_data_b_2_total_amount_nonnegative CHECK (total_amount >= 0);

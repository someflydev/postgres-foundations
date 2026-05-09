DROP TABLE IF EXISTS ecommerce.alter_table_with_existing_data_a_1;
CREATE TABLE ecommerce.alter_table_with_existing_data_a_1 (
    id bigint generated always as identity PRIMARY KEY,
    email text,
    imported_at timestamptz,
    total_amount numeric(12,2)
);

UPDATE ecommerce.alter_table_with_existing_data_a_1
SET imported_at = now()
WHERE imported_at IS NULL;

ALTER TABLE ecommerce.alter_table_with_existing_data_a_1
    ALTER COLUMN email SET NOT NULL,
    ALTER COLUMN imported_at SET DEFAULT now(),
    ALTER COLUMN imported_at SET NOT NULL,
    ALTER COLUMN total_amount SET DEFAULT 0,
    ALTER COLUMN total_amount SET NOT NULL;

ALTER TABLE ecommerce.alter_table_with_existing_data_a_1
    ADD CONSTRAINT alter_table_with_existing_data_a_1_email_unique UNIQUE (email);

ALTER TABLE ecommerce.alter_table_with_existing_data_a_1
    ADD CONSTRAINT alter_table_with_existing_data_a_1_total_amount_nonnegative CHECK (total_amount >= 0);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'ecommerce'
  AND table_name = 'alter_table_with_existing_data_a_1'
ORDER BY table_name;

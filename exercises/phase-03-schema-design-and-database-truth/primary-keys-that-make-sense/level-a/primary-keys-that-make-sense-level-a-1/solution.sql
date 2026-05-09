DROP TABLE IF EXISTS ecommerce.primary_keys_that_make_sense_a_1;
CREATE TABLE ecommerce.primary_keys_that_make_sense_a_1 (
    id bigint generated always as identity,
    sku text,
    name text NOT NULL
);

ALTER TABLE ecommerce.primary_keys_that_make_sense_a_1
    ADD CONSTRAINT primary_keys_that_make_sense_a_1_pkey PRIMARY KEY (id);

ALTER TABLE ecommerce.primary_keys_that_make_sense_a_1
    ALTER COLUMN sku SET NOT NULL;

ALTER TABLE ecommerce.primary_keys_that_make_sense_a_1
    ADD CONSTRAINT primary_keys_that_make_sense_a_1_sku_unique UNIQUE (sku);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'ecommerce'
  AND table_name = 'primary_keys_that_make_sense_a_1'
ORDER BY table_name;

DROP TABLE IF EXISTS ecommerce.primary_keys_that_make_sense_b_2;
CREATE TABLE ecommerce.primary_keys_that_make_sense_b_2 (
    id bigint generated always as identity,
    sku text,
    name text NOT NULL
);

ALTER TABLE ecommerce.primary_keys_that_make_sense_b_2
    ADD CONSTRAINT primary_keys_that_make_sense_b_2_pkey PRIMARY KEY (id);

ALTER TABLE ecommerce.primary_keys_that_make_sense_b_2
    ALTER COLUMN sku SET NOT NULL;

ALTER TABLE ecommerce.primary_keys_that_make_sense_b_2
    ADD CONSTRAINT primary_keys_that_make_sense_b_2_sku_unique UNIQUE (sku);

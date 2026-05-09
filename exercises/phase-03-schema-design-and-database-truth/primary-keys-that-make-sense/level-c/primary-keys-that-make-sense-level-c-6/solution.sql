DROP TABLE IF EXISTS ecommerce.primary_keys_that_make_sense_c_6;
CREATE TABLE ecommerce.primary_keys_that_make_sense_c_6 (
    id bigint generated always as identity,
    sku text,
    name text NOT NULL
);

ALTER TABLE ecommerce.primary_keys_that_make_sense_c_6
    ADD CONSTRAINT primary_keys_that_make_sense_c_6_pkey PRIMARY KEY (id);

ALTER TABLE ecommerce.primary_keys_that_make_sense_c_6
    ALTER COLUMN sku SET NOT NULL;

ALTER TABLE ecommerce.primary_keys_that_make_sense_c_6
    ADD CONSTRAINT primary_keys_that_make_sense_c_6_sku_unique UNIQUE (sku);

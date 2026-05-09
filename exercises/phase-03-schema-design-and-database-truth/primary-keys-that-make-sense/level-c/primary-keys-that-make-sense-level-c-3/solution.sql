DROP TABLE IF EXISTS ecommerce.primary_keys_that_make_sense_c_3;
CREATE TABLE ecommerce.primary_keys_that_make_sense_c_3 (
    id bigint generated always as identity,
    sku text,
    name text NOT NULL
);

ALTER TABLE ecommerce.primary_keys_that_make_sense_c_3
    ADD CONSTRAINT primary_keys_that_make_sense_c_3_pkey PRIMARY KEY (id);

ALTER TABLE ecommerce.primary_keys_that_make_sense_c_3
    ALTER COLUMN sku SET NOT NULL;

ALTER TABLE ecommerce.primary_keys_that_make_sense_c_3
    ADD CONSTRAINT primary_keys_that_make_sense_c_3_sku_unique UNIQUE (sku);

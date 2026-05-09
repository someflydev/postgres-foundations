DROP TABLE IF EXISTS ecommerce.uniqueness_beyond_primary_key_c_3;
CREATE TABLE ecommerce.uniqueness_beyond_primary_key_c_3 (
    id bigint generated always as identity PRIMARY KEY,
    professional_id bigint,
    starts_at timestamptz,
    client_email text
);

ALTER TABLE ecommerce.uniqueness_beyond_primary_key_c_3
    ALTER COLUMN professional_id SET NOT NULL,
    ALTER COLUMN starts_at SET NOT NULL,
    ALTER COLUMN client_email SET NOT NULL;

ALTER TABLE ecommerce.uniqueness_beyond_primary_key_c_3
    ADD CONSTRAINT uniqueness_beyond_primary_key_c_3_professional_starts_unique UNIQUE (professional_id, starts_at);

ALTER TABLE ecommerce.uniqueness_beyond_primary_key_c_3
    ADD CONSTRAINT uniqueness_beyond_primary_key_c_3_client_email_unique UNIQUE (client_email);

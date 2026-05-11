-- What a Schema Is For Level A1
-- Actor/object/operation review.
CREATE SCHEMA IF NOT EXISTS saas AUTHORIZATION saas_migrations;
GRANT USAGE ON SCHEMA saas TO saas_app_readwrite, saas_app_readonly;
-- Evidence: run the admin access-review queries and confirm only intended roles appear.

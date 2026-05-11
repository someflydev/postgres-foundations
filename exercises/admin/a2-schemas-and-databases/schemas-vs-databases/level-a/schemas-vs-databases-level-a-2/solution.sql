-- Schemas vs Databases Level A2
-- Actor/object/operation review.
CREATE SCHEMA IF NOT EXISTS reporting AUTHORIZATION saas_migrations;
GRANT USAGE ON SCHEMA reporting TO saas_app_readonly;
-- Evidence: run the admin access-review queries and confirm only intended roles appear.

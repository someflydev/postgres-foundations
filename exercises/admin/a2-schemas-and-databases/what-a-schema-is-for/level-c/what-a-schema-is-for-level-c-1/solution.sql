-- What a Schema Is For Level C1
-- Repair goal: make schema ownership and schema grants explicit before object grants.
CREATE SCHEMA IF NOT EXISTS saas AUTHORIZATION saas_migrations;
GRANT USAGE ON SCHEMA saas TO saas_app_readwrite, saas_app_readonly;
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

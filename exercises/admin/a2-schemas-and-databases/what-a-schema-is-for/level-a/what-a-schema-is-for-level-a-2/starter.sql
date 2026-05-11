-- Scenario fragment for What a Schema Is For.
CREATE SCHEMA IF NOT EXISTS saas AUTHORIZATION saas_migrations;
GRANT USAGE ON SCHEMA saas TO saas_app_readwrite, saas_app_readonly;

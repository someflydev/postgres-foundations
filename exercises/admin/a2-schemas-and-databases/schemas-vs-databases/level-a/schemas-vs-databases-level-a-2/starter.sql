-- Scenario fragment for Schemas vs Databases.
CREATE SCHEMA IF NOT EXISTS reporting AUTHORIZATION saas_migrations;
GRANT USAGE ON SCHEMA reporting TO saas_app_readonly;

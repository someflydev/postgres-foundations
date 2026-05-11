-- Schemas vs Databases Level C1
-- Repair goal: choose a database only when the operational boundary is worth separate connections, dumps, and restore posture.
CREATE SCHEMA IF NOT EXISTS reporting AUTHORIZATION saas_migrations;
GRANT USAGE ON SCHEMA reporting TO saas_app_readonly;
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

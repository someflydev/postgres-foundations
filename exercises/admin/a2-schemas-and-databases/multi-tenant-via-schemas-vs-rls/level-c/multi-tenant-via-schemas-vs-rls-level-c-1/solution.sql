-- Multi Tenant via Schemas vs RLS Level C1
-- Repair goal: write down tenant count, restore needs, migration fan-out, and reporting queries before choosing the pattern.
CREATE SCHEMA IF NOT EXISTS tenant_acme AUTHORIZATION saas_migrations;
-- Compare this with shared saas.documents protected by RLS policies.
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

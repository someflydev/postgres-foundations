-- Scenario fragment for Multi Tenant via Schemas vs RLS.
CREATE SCHEMA IF NOT EXISTS tenant_acme AUTHORIZATION saas_migrations;
-- Compare this with shared saas.documents protected by RLS policies.

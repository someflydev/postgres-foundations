-- Multi Tenant via Schemas vs RLS Level A1
-- Actor/object/operation review.
CREATE SCHEMA IF NOT EXISTS tenant_acme AUTHORIZATION saas_migrations;
-- Compare this with shared saas.documents protected by RLS policies.
-- Evidence: run the admin access-review queries and confirm only intended roles appear.

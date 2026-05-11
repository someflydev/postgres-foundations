-- Search Path Discipline Level C1
-- Repair goal: schema-qualify references and pin search_path on SECURITY DEFINER functions.
CREATE OR REPLACE FUNCTION saas.secure_lookup(account_id bigint)
RETURNS SETOF saas.accounts
LANGUAGE sql
SECURITY DEFINER
SET search_path = pg_catalog, saas
AS $$ SELECT * FROM saas.accounts WHERE id = account_id $$;
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

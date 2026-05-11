-- Search Path Discipline Level A2
-- Actor/object/operation review.
CREATE OR REPLACE FUNCTION saas.secure_lookup(account_id bigint)
RETURNS SETOF saas.accounts
LANGUAGE sql
SECURITY DEFINER
SET search_path = pg_catalog, saas
AS $$ SELECT * FROM saas.accounts WHERE id = account_id $$;
-- Evidence: run the admin access-review queries and confirm only intended roles appear.

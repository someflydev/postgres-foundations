CREATE OR REPLACE FUNCTION saas.secure_lookup(account_id bigint)
RETURNS SETOF saas.accounts
LANGUAGE sql
SECURITY DEFINER
SET search_path = pg_catalog, saas
AS $$
  SELECT * FROM saas.accounts WHERE id = account_id;
$$;

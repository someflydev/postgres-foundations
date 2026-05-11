CREATE OR REPLACE FUNCTION saas.secure_lookup(account_id bigint)
RETURNS SETOF saas.accounts
LANGUAGE sql
SECURITY DEFINER
AS $$ SELECT * FROM some_table WHERE id = account_id $$;

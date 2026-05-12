CREATE INDEX IF NOT EXISTS accounts_tenant_name_idx
    ON bridge_ext.accounts (tenant_id, account_name);
CREATE INDEX IF NOT EXISTS accounts_search_tsv_gin
    ON bridge_ext.accounts USING gin (search_tsv);
CREATE INDEX IF NOT EXISTS accounts_name_trgm_gin
    ON bridge_ext.accounts USING gin (account_name gin_trgm_ops);
CREATE UNIQUE INDEX IF NOT EXISTS bi_account_order_totals_pk
    ON bridge_ext.bi_account_order_totals (tenant_id, account_id);

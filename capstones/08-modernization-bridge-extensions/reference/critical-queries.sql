SELECT account_id, account_name, ts_rank(search_tsv, plainto_tsquery('english', 'renewal risk')) AS rank
FROM bridge_ext.accounts
WHERE search_tsv @@ plainto_tsquery('english', 'renewal risk')
ORDER BY rank DESC
LIMIT 20;

SELECT account_id, account_name, similarity(account_name, 'acmme') AS score
FROM bridge_ext.accounts
WHERE account_name % 'acmme'
ORDER BY score DESC
LIMIT 20;

SELECT account_id, legacy_customer_id
FROM bridge_ext.accounts
WHERE legacy_customer_id IS NOT NULL
ORDER BY account_id
LIMIT 50;

REFRESH MATERIALIZED VIEW bridge_ext.bi_account_order_totals;

SELECT tenant_id, account_id, order_count, total_value
FROM bridge_ext.bi_account_order_totals
ORDER BY total_value DESC
LIMIT 20;

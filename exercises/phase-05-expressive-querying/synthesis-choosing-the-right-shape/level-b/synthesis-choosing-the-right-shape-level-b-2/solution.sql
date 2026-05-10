WITH tenant_usage AS (
    SELECT tenant_id, date_trunc('day', occurred_at)::date AS usage_date, count(*) AS events
    FROM saas.usage_events
    GROUP BY tenant_id, date_trunc('day', occurred_at)::date
)
SELECT t.slug, u.usage_date, u.events,
       rank() OVER (PARTITION BY u.usage_date ORDER BY u.events DESC) AS daily_rank
FROM tenant_usage u
JOIN saas.tenants t ON t.id = u.tenant_id
ORDER BY u.usage_date, daily_rank, t.slug
LIMIT 40;

\set tenant_id '00000000-0000-0000-0000-000000000001'
\set user_id '00000000-0000-0000-0000-000000000101'
SET app.tenant_id = :'tenant_id';
SET app.user_id = :'user_id';

SELECT count(*) AS active_accounts
FROM accounts
WHERE tenant_id = :'tenant_id'::uuid AND status = 'active';

SELECT stage, count(*) AS deals, coalesce(sum(amount_cents), 0) AS amount_cents
FROM deals
WHERE tenant_id = :'tenant_id'::uuid AND closed_at IS NULL
GROUP BY stage
ORDER BY stage;

SELECT id, full_name, updated_at
FROM contacts
WHERE tenant_id = :'tenant_id'::uuid
ORDER BY updated_at DESC
LIMIT 20;

SELECT id, activity_type, due_at
FROM activities
WHERE tenant_id = :'tenant_id'::uuid
  AND assigned_user_id = :'user_id'::uuid
  AND completed_at IS NULL
ORDER BY due_at
LIMIT 20;

SELECT id, created_at, ts_headline('english', body, plainto_tsquery('english', 'renewal')) AS snippet
FROM notes
WHERE tenant_id = :'tenant_id'::uuid
  AND search_vector @@ plainto_tsquery('english', 'renewal')
ORDER BY created_at DESC
LIMIT 20;

SELECT d.id, d.title, a.name AS account_name, c.full_name AS primary_contact_name,
       count(act.id) AS activity_count, max(n.created_at) AS latest_note_at
FROM deals d
JOIN accounts a ON a.tenant_id = d.tenant_id AND a.id = d.account_id
LEFT JOIN contacts c ON c.tenant_id = d.tenant_id AND c.id = d.primary_contact_id
LEFT JOIN activities act ON act.tenant_id = d.tenant_id AND act.deal_id = d.id
LEFT JOIN notes n ON n.tenant_id = d.tenant_id AND n.deal_id = d.id
WHERE d.tenant_id = :'tenant_id'::uuid
GROUP BY d.id, d.title, a.name, c.full_name
ORDER BY d.opened_at DESC
LIMIT 10;

SELECT id, name
FROM accounts
WHERE tenant_id = :'tenant_id'::uuid
  AND custom_fields @> '{"customer_tier":"gold"}'::jsonb
ORDER BY updated_at DESC
LIMIT 20;

WITH inserted AS (
    INSERT INTO audit_events (tenant_id, actor_user_id, entity_type, entity_id, action, event_data)
    SELECT :'tenant_id'::uuid, NULL::uuid, 'deal', gen_random_uuid(), 'viewed', '{"source":"capstone"}'::jsonb
    WHERE EXISTS (SELECT 1 FROM tenants WHERE id = :'tenant_id'::uuid)
    RETURNING id
)
SELECT ae.id, ae.action, ae.occurred_at
FROM audit_events ae
JOIN inserted i ON i.id = ae.id;

SELECT m.user_id, u.email, m.role, m.active
FROM memberships m
JOIN app_users u ON u.id = m.user_id
WHERE m.tenant_id = :'tenant_id'::uuid
ORDER BY m.role, u.email;

SELECT id, tenant_id, occurred_at
FROM audit_events
WHERE occurred_at < now() - interval '18 months'
ORDER BY occurred_at
LIMIT 100;

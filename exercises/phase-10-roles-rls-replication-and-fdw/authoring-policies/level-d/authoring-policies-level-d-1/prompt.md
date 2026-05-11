# Authoring Policies Level D1

## Setup

Use the Phase 10 SaaS corpus. The incident report says: "RLS is enabled on
`saas.documents`, so tenant data is protected."

## Task

Diagnose this broken policy:

```sql
CREATE POLICY tenant_isolation_select
    ON saas.documents
    FOR SELECT
    USING (true);
```

Write a short repair note that explains why this is not security, how to prove
the leak with `SET app.tenant_id`, and what replacement policy should be used.

## Success Criteria

- Identifies `USING (true)` as a policy that permits every row.
- Includes a cross-tenant verification query.
- Replaces the policy with a tenant predicate based on `current_setting('app.tenant_id')::uuid`.

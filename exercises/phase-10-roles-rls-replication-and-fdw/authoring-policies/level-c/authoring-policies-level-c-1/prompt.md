# Authoring Policies Level C1

## Setup

Seed the Phase 10 SaaS corpus:

```sh
uv run pgfound content seed saas_multi_tenant --phase 10 --reset
```

Connect as `pgfound`, then use `SET ROLE saas_readonly` for the read checks.

## Task

Recreate the tenant isolation policy shape on `saas.documents`.

1. Enable row-level security and force RLS on `saas.documents`.
2. Create `tenant_isolation_select` with `USING (tenant_id = current_setting('app.tenant_id')::uuid)`.
3. Create `tenant_isolation_modify` with the same `USING` predicate and the same `WITH CHECK` predicate.
4. Set `app.tenant_id` to Northwind and show that Northwind documents are visible.
5. Keep the Northwind setting and prove an Acme-filtered query returns 0 rows.
6. Switch `app.tenant_id` to Acme and show Acme documents are visible.

## Success Criteria

- Shows both the policy DDL and the session-scoped verification queries.
- Proves cross-tenant queries return 0 rows.
- Explains why `WITH CHECK` is required for inserts and updates.

# Row-Level Security Playbook

Row-level security belongs in the database when the row boundary is durable
enough that every application path must obey it. In this curriculum the core
example is tenant isolation: `saas.documents` and `saas.audit_events` carry a
`tenant_id`, and application sessions set `app.tenant_id` before ordinary SQL
runs.

## Authoring Checklist

1. Put the tenant or ownership key on the protected table.
2. Index the policy predicate, usually `(tenant_id, id)` or `(tenant_id, time)`.
3. Enable RLS on the table.
4. Add a `USING` predicate for rows an actor may see or affect.
5. Add a `WITH CHECK` predicate for rows an actor may insert or update.
6. Test both same-tenant and cross-tenant reads and writes.
7. Use `FORCE ROW LEVEL SECURITY` when owners should not bypass policies during
   normal application access.

## Tenant Claim Pattern

The Phase 10 seed uses the session setting idiom:

```sql
SET app.tenant_id = '11111111-1111-1111-1111-111111111111';

CREATE POLICY tenant_isolation_select
    ON saas.documents
    FOR SELECT
    USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

This mirrors JWT-like claim propagation: the application authenticates the
request, derives a tenant claim, and sets it on the database session before
running tenant-scoped SQL. With transaction pooling, reset or set the claim for
every transaction so one request cannot inherit another request's tenant.

## Pitfalls

`USING (true)` is not tenant isolation. It makes every row visible to every role
covered by the policy. A read policy without `WITH CHECK` can also leave writes
unprotected. Policies that call functions or cast columns in ways that hide the
indexed key can turn every protected query into avoidable work. Keep policy
predicates boring, indexed, and easy to explain.

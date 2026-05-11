# Authoring Policies

## Problem Framing

Authoring an RLS policy is not just writing a boolean expression. The author
must decide which command the policy covers, which role it applies to, which
existing rows are visible or targetable, and which new row values are allowed.
That is why Phase 10 teaches `USING` and `WITH CHECK` together. A policy that
filters reads but permits cross-tenant inserts is incomplete. A policy that
uses `USING (true)` may satisfy a syntax checklist while providing no
isolation at all.

## Minimal Concept Introduction

`USING` controls which existing rows are visible for `SELECT` and targetable
for `UPDATE` or `DELETE`. `WITH CHECK` controls which proposed rows are valid
for `INSERT` or `UPDATE`. Policies can be written for a specific command, for
all commands, for particular roles, or for all roles. Multiple permissive
policies are ORed; restrictive policies can be used for AND-like behavior.
`FORCE ROW LEVEL SECURITY` makes the table owner obey policies, which is useful
when the application might otherwise connect as an owner role in a lab.

## Worked Example

For `saas.documents`, the teaching policy is intentionally simple:
`tenant_id = current_setting('app.tenant_id')::uuid`. A select policy uses that
predicate in `USING`. A modify policy uses the same predicate in both `USING`
and `WITH CHECK`. The `USING` side says the role may target only rows from its
current tenant. The `WITH CHECK` side says a new or changed row must remain in
that same tenant. A complete exercise proves four facts: same-tenant select
works, cross-tenant select returns zero rows, same-tenant insert works, and
cross-tenant insert or update is rejected.

## Diagnostic Questions

Which command does the policy cover? Is `WITH CHECK` present for writes? Are
there multiple policies whose permissive OR makes the result broader than
expected? Does the policy call a stable expression that can use an index, or
does it wrap the indexed column? Is `current_setting` called with or without
`missing_ok`, and do you want a missing claim to error or silently deny rows?

## Common Pitfalls

The dangerous demo policy is `USING (true)`. It proves that RLS is enabled but
does not restrict rows. Another pitfall is using different read and write
predicates without a clear reason. A third is testing with the table owner and
forgetting owner bypass. Finally, learners sometimes put tenant scoping only in
views or application code; that can be useful, but it is not an RLS policy.

## Explain It Back

Explain a policy by reading it as two gates. `USING` is the gate for existing
rows; `WITH CHECK` is the gate for proposed rows. Then state the session value
the policy depends on and how the application sets it. If the explanation does
not include a negative test, it is not finished. Security claims need evidence,
and in this lesson the evidence is a query or write that crosses tenant
boundaries and fails.

## References and Further Reading

- `docs/rls-playbook.md` for policy cookbook examples.
- `seed-data/packs/saas_multi_tenant/phases/phase-10.sql` for the reference seed.

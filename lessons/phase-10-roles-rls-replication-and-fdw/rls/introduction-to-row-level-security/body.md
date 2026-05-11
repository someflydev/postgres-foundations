# Introduction to Row-Level Security

## Problem Framing

Row-level security answers a different question from table grants. A table
grant says a role may query `saas.documents`; an RLS policy says which document
rows that role may see or change. This matters in multi-tenant systems because
application bugs happen. If the database contains the tenant boundary, a
forgotten `WHERE tenant_id = ...` in application code is less likely to become
a cross-tenant leak. RLS is not free and not universal, but it is the right
tool when the row boundary is durable, security-relevant, and shared across
many access paths.

## Minimal Concept Introduction

`ALTER TABLE ... ENABLE ROW LEVEL SECURITY` turns policy enforcement on for a
table. Policies then define predicates for commands and roles. PostgreSQL
combines table privileges with policies: a role still needs object privileges,
and RLS filters the rows that survive. Table owners and superusers can bypass
RLS unless `FORCE ROW LEVEL SECURITY` is used for the owner case. The Phase 10
seed uses `current_setting('app.tenant_id')::uuid` to represent a tenant claim
set by the application at session or transaction start.

## Worked Example

Seed `saas_multi_tenant` through Phase 10. Set `app.tenant_id` to Northwind's
UUID and query `saas.documents` as a read-only role. The query should return
Northwind documents. Keep the same setting and add `WHERE tenant_id =
'22222222-2222-2222-2222-222222222222'`; the result should be zero rows even
though Acme data exists. Change the setting to Acme's UUID and repeat. This is
the smallest useful RLS proof: same SQL text, different session claim,
different visible rows, and cross-tenant predicates returning nothing.

## Diagnostic Questions

What row attribute carries the boundary? Which role is subject to the policy?
Is the table owner bypassing the policy during the test? Does the policy cover
reads only, or writes too? What happens when `app.tenant_id` is not set? Is the
session setting controlled by trusted application code, and is it reset when
connections are reused?

## Common Pitfalls

RLS is not a substitute for modeling tenant ownership. If rows do not carry
`tenant_id`, the policy becomes awkward or impossible. Another pitfall is
testing as a superuser and concluding the policy is broken. The opposite
mistake is testing only successful same-tenant reads and never proving
cross-tenant denial. Finally, RLS should not hide sloppy grants: the role still
deserves the smallest table, sequence, and function privileges it needs.

## Explain It Back

Explain RLS as a database-enforced row predicate attached to a table. Name the
actor, the table, the boundary column, the policy predicate, and the evidence.
The evidence should include a positive case and a negative case. A good answer
also states where the tenant claim comes from and what happens if the claim is
missing. That explanation connects database security to the application session
model without pretending the database can authenticate HTTP requests by itself.

## References and Further Reading

- `docs/rls-playbook.md` for policy authoring and tenant claim patterns.
- `docs/lab.md` for seeding the Phase 10 SaaS corpus.

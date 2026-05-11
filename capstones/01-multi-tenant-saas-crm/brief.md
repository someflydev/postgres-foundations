# Brief

Produce a complete PostgreSQL 16 design for the SaaS CRM described in the
narrative. Your submission must include schema DDL, index DDL, RLS policy DDL,
critical queries, an operational runbook, and a written defense of the major
tradeoffs. Treat this as a capstone: the reviewer is not looking for one clever
feature, but for a coherent database foundation that composes modeling,
constraints, querying, indexing, security, search, retention, and operations.

The schema must model tenants, users, memberships, accounts, contacts, deals,
activities, notes, and audit events. Use a single database and a single schema.
Tenant-owned rows must carry tenant identity and must be protected by strict
row-level security. The application will set `app.tenant_id` and `app.user_id`
for each request; your policies should make that context meaningful and fail
closed when it is absent. Include the constraints needed to protect core CRM
truth, such as valid lifecycle states, account/contact/deal relationships, and
append-only audit behavior.

You must write 8 to 12 critical queries. Include the ten queries named in
`constraints.md`: dashboard summaries, pipeline reporting, recent contacts,
upcoming activities, tenant-scoped note search, deal detail, bounded JSONB
custom-field filtering, audit event append and review, membership review, and
audit retention candidates. Each query should be scoped to one tenant and should
be written in a way that a reviewer can run and inspect. The dashboard landing
queries should be designed for p95 latency below 200 ms at the stated growth
target.

Indexes must be justified with comments that name the query or workflow they
serve. Do not add indexes only because a column looks important. Use
tenant-leading B-tree indexes where tenant-scoped reads need ordered or
selective access. Use GIN where it is justified for full-text search or bounded
JSONB containment. Explain the write cost of your indexes and what evidence
would make you add, change, or drop one.

Use JSONB only for bounded `custom_fields`. The core CRM facts belong in
relational columns and child tables, not in an unreviewable document blob. Your
writeup must explain when a custom field should be promoted to a column or
normalized table because it has become a reporting dimension, an integrity rule,
or a frequent predicate.

The runbook must cover observation with `pg_stat_statements`, backup and restore
expectations, RLS verification, audit retention maintenance, and what the team
should check before enabling partitioning. Include a practical first-response
path for a slow dashboard query and a customer-reported isolation concern. The
writeup should read like a learner defense: explain why this design fits the
stated scale, why some features are deliberately deferred, and how you would
revisit decisions as the tenant count grows.

Submit the reference-quality artifacts as if another engineer will review them
without a meeting. The DDL should be ordered, named, and runnable. The policies
should be auditable. The queries should be formatted and parameterized clearly
enough that their tenant boundaries are visible. The runbook should avoid vague
advice such as "monitor the database" unless it names what to monitor and how
the signal changes an operational decision.

Your written defense should include "why not" sections. Explain why not
database-per-tenant, why not schema-per-tenant, why not external search today,
why not JSONB for every custom product idea, and why not partition audit events
before volume proves it is worth the maintenance. These answers do not have to
reject those options forever. They should show that the current design is a
deliberate fit for the stated team, deployment target, workload, and deadline.

The reviewer will score both the artifacts and the reasoning. A schema that
passes syntax but cannot be defended is incomplete; a good essay with weak DDL
is also incomplete. The goal is an integrated system that can be run, inspected,
and argued from operational evidence.

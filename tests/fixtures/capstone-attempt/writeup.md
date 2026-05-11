# Reference Writeup

## Position

This design chooses one PostgreSQL database and one schema because the stated
scale does not justify database-per-tenant operations. Fifty tenants today and
500 tenants within a year is meaningful growth, but it is still well inside the
range where ordinary PostgreSQL tables, constraints, tenant-leading indexes, and
row-level security can work. A database-per-tenant model would create backup,
migration, connection, observability, and support overhead before the product
has evidence that isolation or workload shape requires it. A schema-per-tenant
model has many of the same migration and introspection problems. The product
needs strict isolation, but isolation can be enforced at the row level while the
team keeps one operational surface.

The most important invariant is tenant identity on every tenant-owned table.
Accounts, contacts, deals, activities, notes, memberships, and audit events all
carry `tenant_id`. RLS policies compare that value with
`current_setting('app.tenant_id', true)`. The use of `nullif(..., '')::uuid`
means a missing setting does not accidentally match rows. In production, the
application role should not own the tables and should not have `BYPASSRLS`.
Migrations and administrative jobs need their own controlled role and explicit
checks because bypass power is an operational exception, not an everyday
application path.

## Schema choices

The schema keeps durable CRM facts relational. Tenants identify the customer
organization. Users are global identities. Memberships connect users to tenants
and carry tenant-specific roles. Accounts represent companies being sold to,
contacts represent people at those accounts, deals represent opportunities,
activities represent dated follow-up work, notes capture narrative sales
history, and audit events record append-only change history. This grain is
simple enough for a reviewer to inspect and precise enough for the expected
workflows.

The model avoids hiding core relationships in JSONB. Deals point to accounts
and optionally to a primary contact. Activities point to a user and optionally
to a deal or account. Notes point to an author and optionally to a deal or
account. Audit events store the entity type, entity id, action, actor, and a
small JSONB payload for contextual details. The JSONB payload in audit events is
acceptable because audit metadata varies by action and is not the primary
source of relational truth.

`custom_fields` is the only learner-facing JSONB customization pattern. It is
bounded: accounts, contacts, and deals may carry low-cardinality or temporary
customer-defined attributes, but those fields should not become a second schema.
If a custom field becomes a required predicate, a reporting dimension, a
frequent join target, or something with integrity rules, it should be promoted
to a relational column or a tenant-scoped field-definition table with typed
values. The reference solution includes one JSONB GIN index to demonstrate the
pattern for account custom-field containment, but a real team should add such
indexes only for observed hot predicates.

## RLS and isolation

RLS is deliberately applied to tenant-owned tables. The policies use the
application context rather than trusting every query to include a tenant filter.
This protects the common failure mode where a developer writes a query that
looks correct in a single-tenant fixture but leaks rows in production. The
policies cover reads and writes through both `USING` and `WITH CHECK`, so a
session cannot insert a row for a different tenant while operating in one
tenant context.

RLS is not a substitute for application authorization. The membership table and
role values give the application enough information to decide who can administer
members, own deals, or inspect audit events. The database policy shown here
enforces tenant boundaries first. A later design could add role-sensitive RLS
policies, but doing that prematurely can make support and migrations harder to
reason about. The correct first milestone is reliable tenant isolation across
all owned records.

RLS verification should be part of the migration and smoke-test routine. A
small fixture with two tenants should prove that each tenant can see its own
accounts, notes, deals, and audit events, and cannot see or write the other
tenant's records. This test matters more than a prose assurance because RLS
policies are easy to accidentally omit from new tables.

## Query and index strategy

The index set follows the critical query list. The dashboard account summary
uses `(tenant_id, status, updated_at DESC)` because the product lands users in a
tenant-scoped active-account view. Pipeline reporting and deal detail use
tenant/stage and tenant/account indexes. Recently touched contacts use
`(tenant_id, updated_at DESC)`. Upcoming activities use a partial index over
incomplete activities by tenant, assignee, and due time. Audit history uses
tenant and occurred time, while retention candidates use occurred time across
tenants.

The note search uses PostgreSQL core full-text search. A generated `tsvector`
keeps the search document consistent with the note body, and a GIN index
supports text search. The query still includes tenant scope. The reference GIN
index is not tenant-leading because PostgreSQL does not combine tenant equality
inside that same GIN expression in a simple B-tree way; the companion
`notes_tenant_created_idx` helps ordered tenant views, while the search index
serves text matching. If search volume grows, the team should inspect plans and
possibly consider generated per-tenant search patterns, partial indexes for
large tenants, or an external search system only after evidence appears.

The dashboard target is p95 below 200 ms at the one-year scale. That target is
plausible with tenant-leading indexes because each query should touch one
tenant's slice rather than the full dataset. It is still an operational target,
not a guarantee created by DDL. The team should watch `pg_stat_statements`,
application latency histograms, row counts per tenant, and buffer reads. If one
regional tenant becomes much larger than the rest, the next decision may be a
specific index or query rewrite, not a whole new tenancy architecture.

## Audit retention and partitioning

Audit events are append-only. The application should insert events and avoid
updates or deletes except through a controlled retention job. The reference
schema does not implement a trigger to block updates, but the design posture is
clear: audit rows are historical facts. A stricter production version could add
permissions that grant insert/select but not update/delete to the application
role, plus a maintenance role for retention.

Retention is 18 months. Starting unpartitioned is reasonable if event volume is
modest, because premature partitioning adds DDL maintenance, index-management
decisions, and operational sharp edges. Partitioning becomes attractive when
retention deletes become large enough to cause vacuum pressure, when most audit
queries are date-bounded, or when cold partitions can be detached cleanly. A
monthly range partition on `occurred_at` is the likely next step. Maintenance
would create future partitions ahead of time, detach or drop partitions older
than the retention window, and record row counts and timings during the job.

## Why not other options

Separate databases per tenant are deferred because the team has three
engineers, many small tenants, and no hard requirement for tenant-specific
backup or upgrade schedules. Separate schemas per tenant are also deferred
because schema migrations would become harder and query tooling would need to
loop over many schemas. External search is deferred because core FTS supports
the current note-search need and avoids another service. Broad JSONB modeling is
rejected because it would make constraints, joins, and indexing harder exactly
when the product needs reviewable correctness.

The extension posture is intentionally conservative. `pgcrypto` is used for
UUID generation and `pg_stat_statements` is used for observation. Nothing else
is required. If later evidence shows that text search, analytics, or tenant
sharding needs exceed core PostgreSQL, the team should write down the workload
signal, the operational cost, and the migration path before adopting another
extension or service.

## Operations

The runbook starts with visibility. Slow queries should be identified through
application telemetry and `pg_stat_statements`, then reviewed with `EXPLAIN
(ANALYZE, BUFFERS)` in a safe environment. The first questions are whether the
query is tenant-scoped, whether row estimates are plausible, whether the
expected index is used, and whether a specific tenant has become an outlier.

Backups should use the managed provider's continuous backup facility, and the
team should perform restore drills. A backup strategy that has never been
restored is not an operational plan. RLS checks should be automated because a
new table without RLS is an easy regression. Audit retention should run in a
low-traffic window and produce logs that show what was removed or detached.

This is a deliberately boring design. It uses PostgreSQL features that are
portable on managed services and understandable by a small team. It gives the
product enough structure to run a larger-tenant pilot while preserving clear
decision points for future changes.

## Dashboard query posture

The dashboard is the first place where product expectations and database design
meet. A sales rep does not care that the schema is normalized if the landing
page feels slow. The reference design assumes dashboard queries are scoped to a
single tenant and usually to current work: active accounts, open deals,
upcoming incomplete activities, and recently touched contacts. This is why the
indexes lead with `tenant_id` and then the next selective or ordering column.
The goal is not to make every possible CRM report fast. The goal is to make the
known landing workflows predictable while keeping enough write headroom for a
small transactional application.

The p95 target of 200 ms should be measured at the application boundary, but
database evidence still matters. If `pg_stat_statements` shows that the
dashboard summary scans too many rows, the first fix is usually query shape or
index fit. If row estimates are wrong, statistics may need attention. If one
tenant is far larger than the others, a tenant-specific product conversation
may be more useful than a global architecture change. The writeup should make
that judgment explicit: the system is designed to expose signals before it
adopts heavier machinery.

## Search posture

Core PostgreSQL full-text search is intentionally sufficient for this stage.
Notes are rich text, but the stated requirement is tenant-scoped search over
sales history, not a public knowledge engine. A generated search vector keeps
the indexing target stable and avoids recomputing `to_tsvector` for every
query. `ts_headline` in the reference query demonstrates how a learner might
return a useful snippet without adding an external service. Ranking and
language support are intentionally modest.

The rejected alternative is not "search is unimportant." The rejected
alternative is operating a separate search system before the team has evidence
that PostgreSQL FTS is insufficient. If later signals show slow ranking, complex
phrase behavior, high write amplification, or multi-language requirements, the
team can evaluate a search service with real examples. Until then, the core FTS
solution keeps backup, restore, permissions, and tenant isolation in one system.

## Memberships and support access

Memberships are modeled as tenant-specific because a global user may belong to
more than one tenant. The role values are intentionally simple: `admin`,
`manager`, `rep`, and `support`. This is enough to support product decisions
without embedding a full permissions engine in the first capstone. The database
RLS policy enforces tenant boundaries, while the application can use
memberships to decide whether a user may invite teammates, reassign deals, or
view audit history.

Support access deserves special treatment. A SaaS company often needs to help a
customer debug data, but support access can become an isolation risk if it is
implemented as a broad bypass. The reference design does not grant special
support powers at the schema level. A production system should require explicit
tenant context, log support actions, and keep any elevated administrative role
outside the normal request path. That posture fits the principle that RLS
bypass is exceptional and observable.

## Migration posture

The DDL is ordered so a reviewer can apply it to a blank database, but a real
system would still migrate in smaller steps. New nullable columns can be added
before backfills. New constraints can be introduced as `NOT VALID` and then
validated when the data is clean. New indexes on large tables should be created
concurrently in production. New RLS policies should be tested with fixture
tenants before the application role is pointed at them. The writeup should show
that the learner understands the difference between a lab schema and a live
migration plan.

Future schema changes should preserve tenant scope as a review checklist item.
Every new tenant-owned table needs `tenant_id`, a policy, and at least one test
that proves cross-tenant access fails. Every new dashboard query needs a named
workload and an index decision. Every new JSONB field that becomes important
needs a promotion discussion. Those habits keep the design from decaying as the
product grows.

## Partitioning decision detail

Audit partitioning is discussed but not forced. The reason is operational, not
ideological. Partitioning is powerful when data naturally ages out and queries
are time-bounded, but it creates a schedule of future partition creation,
retention jobs, index management, and edge-case testing. At the current stage,
the team may not know audit event volume per tenant or how often customers will
search old audit history. Starting with a clear retention query and an index on
`occurred_at` lets the team gather evidence.

The trigger for partitioning should be concrete. If monthly audit volume grows
large enough that retention deletes take too long, if vacuum on the audit table
starts interfering with current writes, or if support queries almost always
filter by recent time windows, monthly range partitions become easier to
justify. The maintenance plan should create partitions ahead of time, alert if
the next partition is missing, and detach or archive old partitions rather than
issuing huge deletes. This is exactly the kind of "not yet, but know when"
decision the capstone expects.

## Final defense

The design is not the most feature-rich CRM database possible. It is the
smallest coherent foundation that satisfies the stated commitments. It protects
tenant boundaries with RLS, represents core CRM facts relationally, supports the
known critical queries with justified indexes, keeps note search inside
PostgreSQL, and gives audit retention an operational path. It also names what
is deferred and why. That combination is the point of the capstone: correct SQL,
defensible tradeoffs, and an operating model that a three-engineer team can
actually carry.

The most important review question is whether each decision can be traced back
to the scenario. The team has 50 tenants today, not 50,000. It has three
engineers, not a database platform group. It needs strict tenant isolation, but
not tenant-specific infrastructure. It needs note search, but not a dedicated
search team. It needs audit retention, but not immediate partition operations
without volume evidence. The reference solution is shaped by those constraints.

If the business succeeds, this design will not be the final design. That is
acceptable. A good foundation is not one that predicts every future feature; it
is one that keeps today's facts correct and makes tomorrow's changes
reviewable. When a tenant asks for field-level permissions, the team can extend
memberships and authorization. When audit volume grows, the team can introduce
range partitioning. When search logs prove core FTS is insufficient, the team
can evaluate alternatives. Each future step should be tied to workload signals,
not anxiety.

The learner should be able to defend the design under oral review. Why is
`tenant_id` duplicated on child tables instead of inferred through joins?
Because RLS policies and tenant-leading indexes need a direct boundary. Why is
JSONB allowed at all? Because bounded customer fields are real product needs,
but they are kept away from durable CRM truth. Why are indexes not added for
every foreign key and status? Because indexes are write cost and operational
surface, so they should serve named reads. These answers show that the schema
is not merely syntactically valid; it is operationally reasoned.

# Multi-tenant SaaS CRM Narrative

You are joining a three-engineer product team that sells a focused CRM to B2B
sales teams. The product started as a fast internal tool for founder-led sales:
accounts, contacts, deals, activities, notes, and a simple audit trail. It now
has 50 paying tenants, each with about 10 users. The company expects to reach
500 tenants and about 100 users per tenant within a year if the next two sales
quarters go well. That growth is not enterprise scale, but it is large enough
that casual schema choices, missing indexes, and weak tenant boundaries will
become real operational problems.

The tenant mix is uneven. Most customers are single-team startups with three to
fifteen seats. They have one sales pipeline, a few shared accounts, and a small
set of customer-defined fields such as renewal month, source campaign, or
customer tier. One regional firm already has 50 seats, several pipelines, and a
support team that occasionally audits who changed deal ownership or deleted a
note. The product team wants the same database shape to serve both ends of that
range without adding a separate database per tenant, custom schemas, or unusual
managed-service features.

The likely deployment target is Heroku Postgres or RDS PostgreSQL. In product
planning language, the infrastructure rule is "probably Heroku/RDS, so nothing
weird." The team is happy to use ordinary PostgreSQL features that are available
on managed services, but it does not want a design that assumes a specialist
operator, a custom extension build, or a search cluster before there is workload
evidence. PostgreSQL 16 core is the baseline. The only extensions you may
assume are `pgcrypto` and `pg_stat_statements`.

Tenant data must be strictly isolated. The application will set a tenant and
user context at connection checkout, but the database has to enforce the
boundary with row-level security. The team has had enough near misses with
forgotten `WHERE tenant_id = ...` clauses that application filtering alone is
not acceptable. The schema must support memberships and role checks, but it
does not need a full enterprise authorization framework. The product needs a
clear, reviewable answer to the question, "Can one tenant ever read or write
another tenant's CRM records?"

The core workflows are ordinary but important. Sales reps open a dashboard and
expect accounts, open deals, overdue activities, and recently touched contacts
to load quickly. Managers view the pipeline by stage, filter accounts by a few
customer-defined fields, and search rich-text notes. Support staff inspect audit
events when customers ask who changed a record. Audit events are append-only and
must be retained for 18 months. You do not have to implement partition rotation
in the learner starter, but your design and writeup must explain whether
partitioning is appropriate and what maintenance would look like when audit
volume grows.

Notes are rich text, but the product is not ready for an external search
service. The team wants basic note search inside PostgreSQL so a sales rep can
find "renewal risk" or "security review" within one tenant's records. The search
implementation should be good enough to support the pilot and honest enough to
say what it will not do. If ranking, highlighting, or multi-language search
become important later, the team can revisit the decision with production
signals.

The operating tolerance is explicit: "we want not to get paged at 3 AM." That
does not mean nothing can fail. It means the design should avoid avoidable
failure modes for a small team. Constraints should protect business truth.
Indexes should serve named queries rather than every plausible filter.
Operational notes should tell an engineer where to look first when the
dashboard slows down or a customer reports missing audit history. Backup,
restore, and RLS verification should be routine enough that a three-person team
can actually do them.

The deadline is six weeks until a design partner pilot with larger tenants.
The business wants the pilot to feel reliable, not experimental. The engineering
goal is a boring, portable PostgreSQL foundation that can carry the next year of
growth while preserving the option to evolve. Avoid clever architecture. Use
tables, constraints, indexes, row-level security, core full-text search, and a
clear written defense of what is deliberately not being adopted yet.

The product manager will judge the result by whether the team can explain the
design to a customer who asks about isolation and reliability. The engineers
will judge it by whether they can migrate it, debug it, and extend it without
heroics. The sales team will judge it by whether the dashboard and note search
feel fast enough during demos. Those pressures are intentionally mixed, because
the capstone is not a single-topic drill. It asks you to compose the earlier
phases into one system and to defend the operational posture as much as the SQL.

Assume the pilot will reveal ambiguous requirements. Larger tenants may ask for
team-level permissions, custom audit exports, richer text search, or field-level
configuration. Your design should not pretend all of those are solved. It
should make the current commitments safe while leaving clear extension points
for the next conversation.

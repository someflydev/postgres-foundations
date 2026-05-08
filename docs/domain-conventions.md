# Domain Conventions

Reusable domain packs keep PostgreSQL lessons grounded in the same systems as
capstones and review scenarios. A learner should be able to meet `orders`,
`appointments`, or `documents` in an early exercise, then recognize the same
domain when later phases add constraints, indexes, transactions, search, or
partitioning. The schema conventions below keep that reuse predictable.

Table names are lowercase `snake_case`. They use ordinary plural names for
domain entities: `orders`, `appointments`, `documents`, `users`,
`order_items`, and similar names. Join tables should name both sides of the
relationship when that improves clarity, such as `document_tags` or
`project_memberships`. Foreign key columns are named `<ref>_id`, where
`<ref>` is the referenced entity in singular form, such as `customer_id`,
`tenant_id`, `provider_id`, or `document_id`.

Surrogate keys should match the identity needs of the table. High-volume local
tables use `id bigint generated always as identity` because it is compact,
simple to index, and easy for learners to inspect. Entities that must remain
globally unique across systems use `uuid`, generated with `pgcrypto` when the
database owns the identifier. Tenant IDs and externally meaningful references
are common examples. Natural keys can still be modeled with unique constraints,
but they should not be confused with the table's local row identity.

Every durable table includes `created_at` and `updated_at` as `timestamptz NOT
NULL DEFAULT now()`. Lesson SQL may intentionally omit update triggers at first
so learners can see that defaults and automatic maintenance are different
concerns. Time values that describe events or schedules should also use
`timestamptz` unless a lesson is explicitly about local date or wall-clock
modeling.

Soft deletes are discouraged. In this curriculum, delete means delete unless a
lesson names a real retention, audit, undo, or compliance requirement that
justifies a different lifecycle. This keeps early models honest and avoids
teaching a nullable `deleted_at` column as a reflex.

Money is represented as `numeric(12,2)` plus a `currency` column. The numeric
column stores the amount; the currency column makes the unit explicit and keeps
future examples from pretending every system is single-currency by nature.

Large labs and capstones use one schema per domain: `ecommerce`,
`scheduling`, `saas`, `events`, `documents`, and `legacy`. Schema separation
keeps table names readable while making ownership boundaries visible. Small
phase exercises may collapse tables into a shared `pgfound` schema when the
lesson is about a single SQL idea and schema qualification would add noise.
When a lesson does this, it should say so in the setup notes and keep table
names identical to the domain pack.

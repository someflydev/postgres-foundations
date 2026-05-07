# Reusable Domains

Use these domains consistently when authoring lessons and exercises. Later
phases should upgrade familiar systems instead of inventing new semantics for
every feature.

## `ecommerce`

Ecommerce covers customers, products, orders, order items, payments, shipments,
refunds, promotions, and support tickets. It is the default transactional domain
for basic SQL, joins, constraints, reporting, indexing, and operational review.

Core entities: `customers`, `products`, `product_variants`, `orders`,
`order_items`, `payments`, `shipments`, `refunds`, `support_tickets`.

Phase layering: phase 1 reads and changes simple rows; phase 2 joins customers,
orders, items, and products; phase 3 tightens constraints and lookup tables;
phase 4 adds JSONB product attributes and time behavior; phase 5 builds reports;
phase 6 handles payment and inventory races; phase 7 indexes customer and order
queries; phase 8 searches products and tickets; phase 9 may partition audit or
order-event history when volume justifies it; phase 10 adds role-scoped access.

Capstones: `01-multi-tenant-saas-crm` reuses ecommerce-style accounts,
activities, and reporting.

## `scheduling`

Scheduling covers people, resources, services, availability windows,
reservations, cancellations, and conflict rules. It is the recurring domain for
time, ranges, exclusion constraints, and concurrency.

Core entities: `people`, `resources`, `services`, `availability_windows`,
`reservations`, `reservation_events`, `blackout_windows`, `cancellations`.

Phase layering: phase 2 introduces resource and reservation joins; phase 3
adds constraints around status and ownership; phase 4 uses ranges and exclusion
thinking for availability; phase 5 analyzes utilization; phase 6 reproduces
double-booking races; phase 7 indexes lookup and range predicates; phase 9
partitions historical reservation events if volume supports it; phase 10 adds
role boundaries for operators and customers.

Capstones: `02-scheduling-and-availability` is built directly on this domain.

## `saas_multi_tenant`

SaaS multi-tenant covers tenants, users, memberships, accounts, scoped records,
roles, and tenant-specific reporting. It is the main domain for ownership,
tenant isolation, row-level security, and modernization planning.

Core entities: `tenants`, `users`, `tenant_memberships`, `accounts`,
`contacts`, `activities`, `invoices`, `tenant_settings`, `audit_events`.

Phase layering: phase 3 establishes tenant ownership as schema truth; phase 4
adds tenant settings and UUID identity; phase 5 builds tenant reports; phase 6
handles concurrent membership and billing changes; phase 7 indexes tenant
scoped access paths; phase 8 searches contacts and notes; phase 9 may partition
tenant audit events; phase 10 implements roles, grants, and RLS policies.

Capstones: `01-multi-tenant-saas-crm` and `04-modernization-bridge` lean on this
domain.

## `event_heavy_ops`

Event-heavy operations covers append-heavy logs, telemetry, audit events,
workflow transitions, incident records, and retention policies. It makes volume,
write cost, observability, and lifecycle operations concrete.

Core entities: `event_streams`, `events`, `event_payloads`, `actors`,
`devices`, `incidents`, `retention_policies`, `processing_checkpoints`.

Phase layering: phase 5 introduces event analysis and windowed summaries;
phase 6 handles checkpoint and processing races; phase 7 indexes high-volume
filters and recent-event queries; phase 8 searches incident notes; phase 9 is
the main partitioning and retention laboratory; phase 10 discusses replication
and access boundaries for operational data.

Capstones: `03-event-heavy-ops` is built on this domain.

## `document_search`

Document search covers articles, comments, tickets, metadata, authors,
versions, corpora, search sessions, and relevance feedback. It supports JSONB
boundaries, full-text search, ranking, and later extension posture.

Core entities: `documents`, `document_versions`, `authors`, `collections`,
`comments`, `document_metadata`, `search_sessions`, `search_clicks`.

Phase layering: phase 4 introduces JSONB metadata around otherwise relational
documents; phase 5 analyzes versions and engagement; phase 7 indexes metadata
and document filters; phase 8 builds tsvector, tsquery, dictionaries, ranking,
and GIN search; phase 9 may partition search logs; phase 10 controls editor,
reader, and tenant-scoped access.

Capstones: `03-event-heavy-ops` uses this domain for incident and operational
document search.

## `modernization_bridge`

Modernization bridge covers legacy tables, foreign systems, staged migrations,
compatibility views, replication boundaries, and cutover checkpoints. It
appears late because it requires modeling, transactions, indexing, operations,
and access control judgment.

Core entities: `legacy_customers`, `legacy_orders`, `migration_batches`,
`foreign_systems`, `foreign_mappings`, `cutover_checkpoints`,
`reconciliation_results`, `compatibility_views`.

Phase layering: phase 10 introduces FDW, foreign servers, imported schemas,
logical replication concepts, and least-privilege migration roles. Capstone
work layers in schema repair, validation queries, cutover plans, and explicit
"not yet" decisions about sharding, Citus, or extension-heavy migration paths.

Capstones: `04-modernization-bridge` is built directly on this domain.

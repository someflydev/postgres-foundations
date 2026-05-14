# Reference Writeup

## Modeling

The modernization bridge keeps the legacy database as the source of truth for
legacy customers, orders, and products. The new service owns its local schema:
tenants, customer links, new local orders, and cached aggregates. This boundary
matters because the organization does not yet have agreement to migrate the
monolith. A bridge that pretends the migration already happened will create
write conflicts, unclear ownership, and support incidents.

`postgres_fdw` is the right current extension because the new service needs
accurate reads against a limited subset of legacy data. Foreign tables are kept
in a `legacy_fdw` schema so reviewers can see the boundary. Local tables live in
`new_service` and carry tenant identifiers. RLS is enabled on the local tables
because new-service correctness cannot inherit security properties the legacy
database does not have. RLS does not make the foreign legacy tables tenant-safe;
the application must reach legacy rows through local mappings and reviewed
queries.

## Indexes

The materialized view caches legacy order totals by customer. This is useful for
dashboard and list screens that do not need every request to cross the FDW
boundary. The cache is not a source of truth. Its refresh policy should be
explicit: for example, refresh every fifteen minutes during business hours and
on demand after high-value imports. The UI or API contract must say whether the
aggregate is near-real-time or stale by design. If direct FDW reads show a new
order and the cache does not, that is a refresh-policy issue, not a data-loss
incident.

The indexing plan keeps local lookup paths explicit: tenant identifiers,
legacy IDs, and cache refresh predicates should have narrow btree support before
any broader search or analytics feature is considered. Foreign tables are not a
substitute for local indexes on new-service truth.

## Operations

FDW failure modes are operationally important. Network failure, remote
credentials, remote locks, changed legacy schemas, missing predicate pushdown,
and remote query plans can all affect the new service. The runbook starts with
`EXPLAIN (VERBOSE)` for query shape, checks server and user mapping state for
connection failures, and compares direct FDW results with materialized view
freshness when users report stale totals. The team should avoid writing complex
business transactions that require the legacy and new databases to commit as one
unit.

## Extension Posture

`postgres_fdw` is enabled now because it solves a current integration problem
with a bounded operational surface. Logical replication is deferred because the
organization has not settled ownership, identifiers, backfill strategy, conflict
handling, or cutover. Citus is rejected for this stage because the system is not
limited by distributed scale; it is limited by migration sequencing and legacy
ownership. Adding a distributed database layer would make the bridge harder to
operate without solving the current problem.

## Promote to logical replication when X

Promote to logical replication when the migration has a real ownership plan.
The signals are concrete: a target table in the new service has become the
future system of record, identifiers are stable, backfill has been tested,
conflict rules are documented, publication and subscription monitoring is
owned, replication lag has an SLO, and rollback has been rehearsed. At that
point logical replication can move selected tables incrementally while the
monolith still serves unmigrated paths.

## Operational Tolerance

The team can operate FDW reads, local RLS, materialized view refreshes, and
small local write tables. It cannot yet operate a distributed rewrite, complex
cross-database write transactions, or replication cutover under ambiguous
ownership. The bridge therefore ships useful capability now while preserving a
measurable path to migration later.

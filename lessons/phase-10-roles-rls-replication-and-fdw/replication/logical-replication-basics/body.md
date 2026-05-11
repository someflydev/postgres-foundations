# Logical Replication Basics

## Problem Framing

Logical replication moves table changes through publications and
subscriptions. It is useful when the receiving database needs a selected set of
tables rather than a full physical standby. Phase 10 keeps the concept grounded
in PostgreSQL 16 behavior: schemas are not magically migrated, primary keys or
replica identity matter, initial sync is a real step, and replication slots
retain WAL until the subscriber consumes it. This is a table-data movement
tool, not a generic scaling answer.

## Minimal Concept Introduction

The publisher owns a publication: `CREATE PUBLICATION ... FOR TABLE ...`. The
subscriber owns a subscription: `CREATE SUBSCRIPTION ... CONNECTION ...
PUBLICATION ...`. The subscription connects to the publisher, creates or uses a
replication slot, copies initial data when configured to do so, and streams
later changes. The publisher must have `wal_level=logical`. The target table
must already exist on the subscriber with a compatible shape. Updates and
deletes need replica identity so the subscriber can identify changed rows.

## Worked Example

Create `public.replication_lab_events` on `pg`, publish it, and insert one row.
Create the same table on `pg-replica`, then create a subscription pointing at
`host=pg port=5432 dbname=pgfound`. Query the subscriber until the row appears.
Insert a second row on the publisher and observe it on the subscriber. Then
inspect subscription status and the replication slot. The value of the lab is
not the two-row table; it is seeing the lifecycle: publication, target schema,
subscription, initial catch-up, ongoing stream, cleanup.

## Diagnostic Questions

Is `wal_level` logical on the publisher? Does the subscriber table exist? Does
the published table have a primary key or replica identity? Did initial sync
finish? Is the subscription enabled? Is a replication slot retaining WAL? Is
lag growing, stable, or shrinking? Which side owns the error message: publisher
connectivity, subscriber schema, or row identity?

## Common Pitfalls

Logical replication can be "working" while lag grows. Slots retain WAL, so an
unhealthy subscriber can become a storage problem on the publisher. Another
mistake is expecting DDL to replicate like physical WAL replay. If a column is
added on the publisher, the subscriber shape still needs planning. A third
mistake is using logical replication for cross-region low-latency reads without
thinking about lag and conflict expectations.

## Explain It Back

Explain logical replication by naming the publication, subscription, slot,
tables, initial sync, and lag observation. Then contrast it with physical
replication: logical is table-oriented and flexible, physical is cluster-level
WAL replay. A good answer includes cleanup: dropping a subscription and
publication intentionally so no abandoned slot keeps WAL forever.

## References and Further Reading

- `docs/logical-replication-playbook.md` for setup and operational checks.
- `docs/lab.md` for starting `pg-replica`.

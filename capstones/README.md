# Capstones

The capstones combine schema design, querying, operations, security, and
extension-selection judgment. Each one asks for PostgreSQL work plus a written
defense.

## 01 Multi-tenant SaaS CRM

[01-multi-tenant-saas-crm](01-multi-tenant-saas-crm/) asks for a portable SaaS
CRM with strict RLS, core full-text search, audit retention, dashboard queries,
and an operational posture suitable for managed PostgreSQL.

## 02 Scheduling Availability

[02-scheduling-availability](02-scheduling-availability/) asks for appointment
scheduling with exclusion constraints, time-zone aware availability, waitlist
flows, concurrency safety, and a clear stance on deferred geo and partitioning
features.

## 03 Event-heavy Operations

[03-event-heavy-ops](03-event-heavy-ops/) asks for a PostgreSQL 16 event store
for device operations with range partitioning, BRIN and btree indexes, retention
maintenance, pg_stat_statements-driven triage, and explicit TimescaleDB-later
criteria.

## 04 Modernization Bridge

[04-modernization-bridge](04-modernization-bridge/) asks for a new service that
uses `postgres_fdw` to read selected legacy data, writes local truth safely,
enforces RLS on the new side, caches a legacy aggregate with a stated freshness
contract, and explains when logical replication becomes the right migration
step.

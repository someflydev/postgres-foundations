# Postgres FDW Introduction

## Problem Framing

`postgres_fdw` lets PostgreSQL query tables from another PostgreSQL database.
In Phase 10 the "remote" database is a loopback server pointing at the same lab
instance. That may sound artificial, but it is a realistic teaching pattern:
learners can practice extension setup, server definitions, user mappings,
foreign table imports, and local/foreign joins without needing another managed
database. FDW is federation, not replication. Every query still reaches across
the server boundary at execution time.

## Minimal Concept Introduction

The setup has four parts. `CREATE EXTENSION postgres_fdw` installs the wrapper.
`CREATE SERVER` defines the remote PostgreSQL endpoint. `CREATE USER MAPPING`
stores credentials for a local role to connect to that endpoint. `IMPORT
FOREIGN SCHEMA` creates foreign table definitions in a local schema. A foreign
table has local metadata but remote storage. PostgreSQL can push some filters,
joins, and aggregates to the remote side, but not every expression is pushdown
friendly. `EXPLAIN VERBOSE` helps reveal what remote SQL will run.

## Worked Example

Seed `modernization_bridge` through Phase 10. The seed creates legacy CRM-style
tables under `legacy`, a loopback server named `legacy_loopback`, and foreign
tables under `legacy_fdw`. Query `legacy_fdw.crm_accounts_1998` and then join it
to local `legacy.customer_mappings`. The result maps external customer numbers
to canonical customer references. This is the smallest useful modernization
bridge: leave the legacy shape visible, add a local mapping table, and compose a
query that lets modern code reason over both worlds.

## Diagnostic Questions

Is the extension installed? Does the server point to the intended database and
port? Which local role owns the user mapping? Are credentials appropriate for a
lab, or would they need a secret-management story in production? Did
`IMPORT FOREIGN SCHEMA` create the expected tables? Does `EXPLAIN VERBOSE` show
remote filters being pushed down, or is PostgreSQL fetching too many rows?

## Common Pitfalls

Treating FDW like a local table is the core mistake. Network latency, remote
permissions, transaction behavior, and pushdown limits all matter. Another
pitfall is importing an entire legacy schema when only a few tables are needed.
That creates a false sense of modernization. A third is storing broad remote
credentials in user mappings without thinking about who can use the mapping.

## Explain It Back

Explain FDW by naming what is local metadata and what is remote data. Then name
the server, user mapping, foreign schema, and query that proves the bridge
works. A strong explanation also says when FDW is a starting point rather than
an end state: useful for exploration and phased migration, risky as an
unbounded dependency for hot transactional paths.

## References and Further Reading

- `docs/lab.md` for the local PostgreSQL service details.
- `seed-data/packs/modernization_bridge/phases/phase-10.sql` for the loopback setup.

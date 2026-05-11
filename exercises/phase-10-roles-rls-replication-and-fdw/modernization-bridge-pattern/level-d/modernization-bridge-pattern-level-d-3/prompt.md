# Modernization Bridge Pattern Level D3

## Setup

Use the `legacy-fdw-stale-matview` scenario.

## Task

Critique a modernization bridge that reads through FDW but also serves a cached
materialized aggregate. Show why the cache can be stale after the legacy side
changes, then propose a refresh policy and user-facing freshness contract.

## Success Criteria

- Identifies the stale materialized-view behavior.
- Distinguishes direct legacy reads from cached aggregate reads.
- Names an operational refresh policy.
- Explains why logical replication is not automatically the first fix.

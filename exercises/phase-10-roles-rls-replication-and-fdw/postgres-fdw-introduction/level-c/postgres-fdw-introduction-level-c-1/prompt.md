# Postgres FDW Introduction Level C1

## Setup

Seed the modernization bridge through Phase 10:

```sh
uv run pgfound content seed modernization_bridge --phase 10 --reset
```

## Task

Use the loopback FDW bridge to query legacy CRM account data.

1. Confirm `postgres_fdw` is installed.
2. Confirm the `legacy_loopback` server and user mapping exist.
3. Run `IMPORT FOREIGN SCHEMA` for a small legacy table if it is not already present.
4. Join local `legacy.customer_mappings` to foreign `legacy_fdw.crm_accounts_1998`.
5. Return canonical customer reference, legacy company name, and last invoice total.

## Success Criteria

- Uses a foreign table under `legacy_fdw`.
- Joins local mapping data to foreign legacy data.
- Explains why this is federation rather than replication.

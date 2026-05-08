# Modernization Bridge

## What this domain is

The modernization bridge domain models data moving from an older system into clearer PostgreSQL structures. It gives learners messy but controlled legacy rows that can be inspected, joined, cleaned, and compared with modern target tables. Later phases use it for migrations, compatibility views, foreign-data-style reasoning, and capstone planning.

## Core entities

- Legacy customers: imported customer rows with source-system identifiers.
- Legacy orders: imported order rows with external references and money fields.
- Import batches: load metadata introduced when joins and auditability matter.
- Customer mappings: source-to-target identity bridges used in migration lessons.

## Recurring scenarios

- Phase 0: model legacy identities, import batches, mappings, duplicated facts,
  and migration lifecycle events on paper before SQL.
- Phase 1: inspect imported rows and spot inconsistent source fields.
- Phase 2: join rows to import batches and mappings.
- Phase 3: tighten constraints after profiling legacy data.
- Phase 4: choose PostgreSQL types for external identifiers and flexible source metadata.
- Phase 8: reason about operational migration runs and rollback evidence.
- Phase 10: design a modernization capstone with staged compatibility.

## Non-goals

This pack does not implement a complete ETL platform, change-data-capture pipeline, or cross-database federation layer. It keeps migration facts visible in ordinary PostgreSQL tables.

## Naming and schema overview

Large labs use the `legacy` schema. Small exercises may collapse these tables into `pgfound`. Tables: `legacy_customers`, `legacy_orders`, `import_batches`, and `customer_mappings`.

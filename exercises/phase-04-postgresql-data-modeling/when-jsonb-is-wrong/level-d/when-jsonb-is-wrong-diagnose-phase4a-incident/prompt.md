# Diagnose and repair the incident: When JSONB Is Wrong

## Setup

Use the PostgreSQL Foundations lab and the `ecommerce` seed pack at phase 4a.

## Given

Use the Phase 4a seed data for `ecommerce`. The lesson topic is JSONB misuse.

## Task

A report filters `orders.metadata ->> 'channel'` every hour. Propose the migration that extracts `channel` to a proper column and write the rewritten query. This incident could violate reporting correctness if typos remain hidden.

## Success Criteria

- The answer names the modeled fact.
- The answer includes both a good-fit and bad-fit example when prose is requested.
- The answer stays inside the Phase 4a boundary.

## Estimated Time

45 minutes.

# Migrate roles out of an array: What Arrays Are Bad For

## Setup

Use the PostgreSQL Foundations lab and the `ecommerce` seed pack at phase 4b.

## Given

Use the lesson topic: user_roles text[] as a deliberately weak design.

## Task

A schema stores `user_roles` as `roles text[]`. Diagnose why revocation, audit, and role metadata are painful. Propose a child table and write the migration shape.

## Success Criteria

- Name the modeled fact before the PostgreSQL feature.
- Include both a good-fit and bad-fit example when prose is requested.
- Stay inside the Phase 4b boundary.

## Estimated Time

See `exercise.json`.

# SaaS Multi-Tenant

## What this domain is

The SaaS multi-tenant domain models a small business application with many customer organizations in one PostgreSQL database. It is useful because nearly every table carries tenant context, and mistakes can leak data across boundaries. Early phases use it for filtering and joins; later phases use it for constraints, transactions, roles, and operational design.

## Core entities

- Tenants: customer organizations with globally unique identifiers.
- Users: people who belong to a tenant.
- Projects: tenant-owned workspaces or records.
- Memberships: user-to-project access rows introduced when join paths matter.

## Recurring scenarios

- Phase 0: model tenants, users, projects, memberships, ownership boundaries,
  and tenant-local identity on paper before SQL.
- Phase 1: filter data by tenant and status.
- Phase 2: join users, tenants, and projects without crossing boundaries.
- Phase 3: enforce tenant-scoped uniqueness, membership access-level boundaries,
  and reference-backed billing country and currency facts.
- Phase 6: reason about updates that must stay tenant-local.
- Phase 8: design operational admin queries without bypassing isolation.
- Phase 10: use tenant-aware capstone review criteria.

## Non-goals

This pack does not implement billing, OAuth, SSO, audit products, or a complete row-level-security framework. Those topics appear later only when the prompt sequence asks for them.

## Naming and schema overview

Large labs use the `saas` schema. Small phase exercises can collapse the same tables into `pgfound` for simpler examples. Tables: `tenants`, `users`, `projects`, and `project_memberships`.

Phase 05 volume: at least 50 tenants, each with 5-200 generated users, plus a saas.usage_events table with at least 6000 events for lateral-join and window-function drills.

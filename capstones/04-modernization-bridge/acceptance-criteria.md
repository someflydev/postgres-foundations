# Acceptance Criteria

- Schema separates legacy foreign tables from new-service local ownership.
- FDW wiring is documented and includes `IMPORT FOREIGN SCHEMA`.
- Materialized view cache has a refresh policy and staleness warning.
- RLS protects local tenant-owned tables.
- Critical queries include FDW reads, local writes, cache reads, and diagnostics.
- Writeup includes FDW failure modes, logical-replication promotion criteria,
  Citus deferral, and an extension posture section.

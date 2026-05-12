# Acceptance Criteria

- Reference schema creates the logistics entities, spatial columns, breadcrumb partition root, and note search vector.
- Index artifact includes GiST spatial indexes, GIN FTS index, and partition-friendly time indexes.
- Critical queries cover zone-bounded top-N couriers, SLA reporting, breadcrumb replay, and note search.
- Runbook names pg_stat_statements triage, partition maintenance, spatial index maintenance, and retention.
- Writeup includes at least one now, later, and avoid-for-now extension decision.

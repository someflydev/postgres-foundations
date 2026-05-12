# Brief

Build the schema, indexes, partitioning plan, critical queries, operational runbook, and written defense for a geo-enabled logistics platform.

Required capabilities:

- Store couriers, vehicles, service zones, deliveries, SLA facts, and historical breadcrumbs.
- Use PostGIS for service-zone polygons and breadcrumb points.
- Use pg_partman-managed time partitioning for breadcrumbs at about 100 million rows per year.
- Use GiST indexes for spatial access and GIN full-text indexes for delivery notes.
- Provide queries for zone-bounded top-N couriers, SLA reporting, breadcrumb replay, and note search.
- Include an operational runbook that starts with pg_stat_statements triage.
- Explain why pgvector is not needed now.

The writeup must contain a principled extension posture with now, later, and avoid-for-now decisions.

# Constraints

- PostGIS is required.
- pg_partman is required for breadcrumb partition management.
- Breadcrumb partitioning must be justified by row volume, retention, and replay query shape.
- Delivery note search uses core full-text search.
- Service-zone and breadcrumb access use GiST spatial indexes.
- pg_stat_statements must be part of the operational runbook.
- pgvector must be explicitly rejected unless future workload signals prove semantic retrieval is needed.

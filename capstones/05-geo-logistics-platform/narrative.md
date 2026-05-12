# Geo-enabled Logistics Platform

A regional delivery company is moving its operational data model into PostgreSQL. Dispatch scoring still runs outside the database, but PostgreSQL owns the facts that make dispatch auditable: couriers, vehicles, deliveries, service zones, GPS breadcrumbs, and SLA outcomes. The target scale is 1,000 to 2,000 couriers, 10,000 to 20,000 deliveries per day, and roughly 100 million breadcrumb rows each year.

The hard part is not drawing a map. The hard part is deciding which spatial, partitioning, search, and operational features belong in the first production version. PostGIS is required because the system must answer polygon containment and proximity questions correctly. Breadcrumbs need a partitioning plan that can survive retention work and replay queries. Delivery notes need ordinary PostgreSQL full-text search, not a semantic search subsystem.

Your design should be explicit about the boundary between the dispatch algorithm and the database. PostgreSQL should provide fast, explainable data access for zones, courier availability, SLA reporting, and breadcrumb replay. It should not become an unreviewed routing engine.

# E3 PostGIS

PostGIS belongs in a PostgreSQL design when geography or geometry is a real domain: containment, intersection, distance, SRID transforms, and spatial indexes are part of the workload. A latitude and longitude column by itself is not enough evidence. Start with the business predicate, decide whether `geometry` or `geography` is correct, and prove the query shape with EXPLAIN before adding the extension to a production cluster.

Use the separate `postgis` Compose profile for labs: `docker compose --profile postgis up -d postgis` from the `docker/` directory. The main `pg` service stays on `postgres:16` so ordinary lessons do not inherit PostGIS image size, upgrade coupling, or extension assumptions.

Operational review must cover backup size, restore time, managed-service support, extension version, application SQL surface area, and a rollback plan. The right answer is often not yet when the workload only needs display coordinates, bounding-box prefilters, or geocoding handled outside the database.

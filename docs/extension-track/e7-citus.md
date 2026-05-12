# E7 Citus

Citus is late-stage distributed PostgreSQL. Use it only after the team has a proven distribution key, workload locality that fits sharding, and operational comfort with coordinator and worker failure modes. The lab profile uses `citusdata/citus:12.1` with one coordinator and two workers on host port 5439.

Start it with `docker compose -f docker/docker-compose.yml --profile citus up -d citus-coordinator citus-worker-1 citus-worker-2`. Verify with `SELECT * FROM citus_get_active_worker_nodes();` on `postgresql://pgfound:pgfound@localhost:5439/pgfound`.

Prefer not yet when the request is sharding as performance insurance, sharding without a tenant or entity locality model, or sharding to compensate for missing indexes and query review.

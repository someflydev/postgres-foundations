# pg_partman

pg_partman operationalizes core PostgreSQL partitioning. It helps with future partition creation, premake windows, retention, and scheduled maintenance. It does not remove the need to choose a good partition key, understand indexes, or test retention with production-like data.

The lab profile builds `docker/pg-with-partman/Dockerfile` and exposes PostgreSQL on host port 5440. Start it with `docker compose -f docker/docker-compose.yml --profile pgpartman up -d pgpartman`, then inspect `partman.part_config` and run `partman.run_maintenance_proc()` during exercises.

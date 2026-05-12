# Lab Operator Guide

The PostgreSQL lab runs in Docker so learners do not need a local PostgreSQL
install. The main service is `pg`, backed by the named Docker volume
`pgfound-data`. From the repository root, the Makefile wraps the Compose file
under `docker/`; direct Docker users can run the same commands with
`docker compose -f docker/docker-compose.yml`.

Start the main lab database with:

```sh
make lab-up
```

The direct Compose equivalent is:

```sh
docker compose -f docker/docker-compose.yml up -d pg
```

The database listens inside Docker on port 5432 and on the host at
`localhost:55433`. The default lab credentials are `pgfound` / `pgfound`, with
database `pgfound`; copy `.env.example` to `.env` only when you need to override
those local defaults.

Connect with psql through the running container:

```sh
make lab-psql
```

Or connect from a host psql client:

```sh
psql "postgresql://pgfound:pgfound@localhost:55433/pgfound"
```

Stop the lab without deleting the database volume:

```sh
make lab-down
```

Reset the lab completely with:

```sh
make lab-nuke
```

That command runs `docker compose down -v`; the `-v` flag destroys the
persisted `pgfound-data` database volume. Use it when you want init scripts to
run again from a clean database.

For throwaway experiments, start the sandbox profile:

```sh
make lab-sandbox-up
```

This starts the normal `pg` service and an additional `pg-sandbox` service on
host port 55434. The sandbox uses an anonymous volume and has no init scripts,
so it is suitable for disposable scratch work. It is not the right target for
concurrency labs because its state is intentionally temporary and separate
from the main lesson database.

Concurrency labs use the normal `pg` service. Open two host terminals and
connect both to `localhost:55433`, then use explicit transaction blocks such as
`BEGIN;`, `SELECT ... FOR UPDATE;`, and delayed `COMMIT;` calls to hold locks
open while the second session observes blocking, isolation behavior, or
deadlock handling. Keeping both sessions on the main `pg` service ensures they
share the same persisted database and lesson setup.

Phase 10 logical replication labs add a second PostgreSQL 16 service behind the
`replication` profile:

```sh
docker compose -f docker/docker-compose.yml --profile replication up -d
```

The publisher is `pg` on the Compose network. The subscriber target is
`pg-replica`, exposed on host port 5435. Both services start with
`wal_level=logical`. The subscriber is an independent PostgreSQL instance used
for publication/subscription practice; it is not a physical replica.

Minimal publisher/subscriber flow:

```sql
-- On pg:
CREATE TABLE IF NOT EXISTS public.replication_lab_events (
    id bigint PRIMARY KEY,
    event_name text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE PUBLICATION phase10_pub FOR TABLE public.replication_lab_events;
INSERT INTO public.replication_lab_events VALUES (1, 'publisher-ready', now());

-- On pg-replica:
CREATE TABLE IF NOT EXISTS public.replication_lab_events (
    id bigint PRIMARY KEY,
    event_name text NOT NULL,
    created_at timestamptz NOT NULL
);

CREATE SUBSCRIPTION phase10_sub
    CONNECTION 'host=pg port=5432 dbname=pgfound user=pgfound password=pgfound'
    PUBLICATION phase10_pub;

SELECT * FROM public.replication_lab_events ORDER BY id;
```

Stop the profile with
`docker compose -f docker/docker-compose.yml --profile replication down`. Add
`-v` only when you intentionally want to remove the replication lab volumes.

Admin A3 authentication labs include a separate HBA overlay service behind the
`hba_overlay` profile:

```sh
docker compose -f docker/docker-compose.yml --profile hba_overlay up -d pg-hba-overlay
```

It listens on host port 55435 by default and mounts
`docker/hba_overlay/pg_hba.conf` as the active authentication file. Use it for
`pg_hba_file_rules` and SCRAM rule-ordering drills without changing the normal
`pg` service.

Admin A3 pooling labs include PgBouncer behind the `pooling` profile:

```sh
docker compose -f docker/docker-compose.yml --profile pooling up -d
psql "postgresql://pgfound:pgfound@localhost:6432/pgfound" -c "SELECT 1;"
```

The PgBouncer configuration lives under `docker/pgbouncer/` and points at the
normal `pg` service on the Compose network. It uses transaction pooling so
learners can observe how session-scoped state differs from a direct PostgreSQL
connection.

Extension-track labs keep specialized images out of the normal `pg` service.
PostGIS runs behind the `postgis` profile with a pinned
`postgis/postgis:16-3.4` image:

```sh
docker compose -f docker/docker-compose.yml --profile postgis up -d postgis
psql "postgresql://pgfound:pgfound@localhost:5436/pgfound" \
  -c "CREATE EXTENSION IF NOT EXISTS postgis; SELECT PostGIS_Version();"
```

Seed the PostGIS logistics domain against that profile with:

```sh
PGFOUND_DB_URL=postgresql://pgfound:pgfound@localhost:5436/pgfound \
  uv run pgfound content seed logistics_geo --phase 1 --reset
```

pgvector runs behind the `pgvector` profile with a pinned
`pgvector/pgvector:pg16` image:

```sh
docker compose -f docker/docker-compose.yml --profile pgvector up -d pgvector
psql "postgresql://pgfound:pgfound@localhost:5437/pgfound" \
  -c "CREATE EXTENSION IF NOT EXISTS vector; SELECT '[1,0,0]'::vector <-> '[0,1,0]'::vector;"
```

The `document_search` phase 08 seed adds deterministic fake embeddings only
when the `vector` extension is available. Those vectors are placeholders for
pgvector mechanics, not meaningful semantic embeddings.

The lab currently uses a single PostgreSQL superuser role, `pgfound`, for
simplicity. Phase 10 introduces role design and least-privilege practice;
deeper operational separation remains part of the later admin track.

If port 55433 is already in use, set `POSTGRES_PORT` in `.env` and restart the
service. If the sandbox port 55434 is occupied, set `POSTGRES_SANDBOX_PORT`. If
the HBA overlay port 55435 is occupied, set `POSTGRES_HBA_OVERLAY_PORT`. If
the PgBouncer port 6432 is occupied, set `PGBOUNCER_PORT`. If the PostGIS port
5436 is occupied, set `POSTGIS_PORT`. If the pgvector port 5437 is occupied,
set `PGVECTOR_PORT`. If init scripts do not run, confirm you reset with
`make lab-nuke`; PostgreSQL entrypoint scripts run only when the data directory
is empty. If the container reports permission issues reading init scripts,
check that files under `docker/initdb/` are readable by Docker. Tail logs with:

```sh
make lab-logs
```


Phase 8 full-text search labs also install `unaccent` at database initialization. If you add it to an existing lab volume, reset with `make lab-nuke` or run `CREATE EXTENSION IF NOT EXISTS unaccent;` manually before using the multi-language and unaccent exercises.

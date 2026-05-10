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

The lab currently uses a single PostgreSQL superuser role, `pgfound`, for
simplicity. Role design, least privilege, and operational separation arrive
later in PROMPT_24 and PROMPT_31.

If port 55433 is already in use, set `POSTGRES_PORT` in `.env` and restart the
service. If the sandbox port 55434 is occupied, set `POSTGRES_SANDBOX_PORT`. If
init scripts do not run, confirm you reset with `make lab-nuke`; PostgreSQL
entrypoint scripts run only when the data directory is empty. If the container
reports permission issues reading init scripts, check that files under
`docker/initdb/` are readable by Docker. Tail logs with:

```sh
make lab-logs
```


Phase 8 full-text search labs also install `unaccent` at database initialization. If you add it to an existing lab volume, reset with `make lab-nuke` or run `CREATE EXTENSION IF NOT EXISTS unaccent;` manually before using the multi-language and unaccent exercises.

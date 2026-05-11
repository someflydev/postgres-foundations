# A3 Auth And Pooling Playbook

Authentication and connection management are operational primitives. A useful
change record names the role, database, connection path, server setting, and
the evidence that proves the current behavior.

## pg_hba.conf

Read `pg_hba.conf` as ordered policy. The first matching line wins. Use
`local` for Unix socket connections, `host` for TCP, and `hostssl` when TLS is
required. In the lab, the `hba_overlay` profile starts a separate PostgreSQL
service with `docker/hba_overlay/pg_hba.conf` mounted as the active HBA file:

```sh
docker compose -f docker/docker-compose.yml --profile hba_overlay up -d pg-hba-overlay
```

Verify parsed rules with:

```sql
SELECT line_number, type, database, user_name, address, auth_method, error
FROM pg_hba_file_rules
ORDER BY line_number;
```

## Auth Methods

Use `trust` only for disposable local surfaces. Prefer `scram-sha-256` over
`md5` for password authentication. Peer authentication is an operating-system
identity mapping. Certificate authentication can be strong, but it adds
certificate issuance, rotation, revocation, and hostname verification work.

## Credential Rotation

Rotate app credentials with overlap: create or update the replacement login,
grant the same group-role membership, deploy the new secret, verify new
sessions, drain old sessions, and retire the old secret. Avoid single-step
rotations that require every app instance to change at once.

## Connection Hygiene

Every application connection should set `application_name`. Bound work with
`statement_timeout` and use `idle_in_transaction_session_timeout` to prevent
forgotten transactions from holding locks and xmin. Treat `max_connections` as
a capacity envelope, not a tuning knob to raise during every incident.

## Pooling

Pooling reduces backend churn and caps server-side connection count. Session
pooling preserves session state. Transaction pooling returns the server
connection after each transaction, which can break session-scoped `SET` state
and prepared statements. Statement pooling is stricter and fits fewer apps.

Start the PgBouncer lab profile with:

```sh
docker compose -f docker/docker-compose.yml --profile pooling up -d
psql "postgresql://pgfound:pgfound@localhost:6432/pgfound" -c "SELECT 1;"
```

The prompt 32 PgBouncer service is scaffolding for diagnosis exercises and the
later deep dive. Do not treat it as a production configuration.

## Connection Storms

When PostgreSQL reaches `max_connections`, new sessions fail while existing
sessions may still consume CPU, memory, and locks. Recover by preserving an
admin path, inspecting `pg_stat_activity`, terminating safe idle sessions,
reducing app concurrency, and adding backpressure or pooling after the incident.

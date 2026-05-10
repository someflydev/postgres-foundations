# Concurrency Harness

The concurrency harness runs deterministic multi-session PostgreSQL scripts
against the lab database. It supports exercise authoring, answer checks, and
repeatable interview-style traces. It does not replace the Phase 6 requirement
that learners run each race family by hand in real `psql` terminals.

## Run Scenarios

List available scenarios:

```sh
uv run pgfound lab concurrency list
```

Run one scenario:

```sh
uv run pgfound lab concurrency run scenarios/concurrency/inventory-lost-update.yaml
```

Use `--on-fail pause` while authoring to keep harness connections open after a
mismatch. Open another `psql` session to inspect locks, rows, and transaction
state, then press Enter in the harness terminal to close the sessions.

Emit a normalized transcript for authoring review:

```sh
uv run pgfound lab concurrency record scenarios/concurrency/inventory-lost-update.yaml
```

## Scenario Shape

Scenarios live under `scenarios/concurrency/`. Each file declares named
sessions, setup SQL, ordered steps, and optional teardown SQL:

```yaml
name: inventory-lost-update
sessions:
  A: {role: pgfound, database: pgfound}
  B: {role: pgfound, database: pgfound}
setup_sql: |
  CREATE SCHEMA IF NOT EXISTS pgfound_harness;
steps:
  - session: A
    sql: "BEGIN;"
  - session: A
    sql: "SELECT quantity_on_hand FROM pgfound_harness.inventory;"
    expect:
      rows: [{quantity_on_hand: 10}]
teardown_sql: |
  DROP TABLE IF EXISTS pgfound_harness.inventory;
```

Supported expectations:

- `rows`: exact row dictionaries. Order is ignored unless `ordered: true`.
- `rowcount`: affected row count.
- `error_code`: expected PostgreSQL SQLSTATE, such as `40001` or `40P01`.
- `blocks`: verifies that a statement does not complete before the timeout.
- `timeout_seconds`: per-step timeout override.

Each session uses a dedicated open psycopg connection and worker thread, so a
blocked statement does not stop the driver from advancing another session.

## Exercise Checks

For `expected_output_shape: multi_session_trace`, `pgfound exercise run --check`
runs the scenario named by `lab_harness_profile`. If the scenario text contains
`${LEARNER_SQL}`, the runner replaces that placeholder with the learner answer
SQL from `--answer` or `tmp/answers/<exercise-id>.sql` before execution.

Standalone library scenarios do not need the placeholder. They can be run
directly with `pgfound lab concurrency run`, but exercise check profiles must
point to a scenario that includes `${LEARNER_SQL}` so the submitted answer is
actually evaluated.

# PgBouncer Deep Operations

PgBouncer reduces backend connection pressure, but pool mode matters. Session pooling preserves session behavior with less multiplexing. Transaction pooling improves reuse while breaking assumptions around session state, temporary tables, some prepared statement behavior, and LISTEN/NOTIFY. Statement pooling is narrower still.

Use the existing `pooling` profile from `docs/lab.md`. Treat `SHOW POOLS`, `SHOW CLIENTS`, `SHOW SERVERS`, and exported metrics as operational evidence, not decorative status output. Keep long-lived listener connections and other session-scoped workflows on a direct or session-pooled path.

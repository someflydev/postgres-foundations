# Arrays Over Child Tables

Arrays are a good PostgreSQL fit for small, bounded sets that travel with the
row: product tags, supported notification channels, or a compact list of labels.
They become an anti-pattern when each element wants identity, lifecycle,
metadata, permissions, audit history, or joins.

The common failure mode is a column such as `user_roles text[]`. It looks simple
until someone asks when a role was granted, who revoked it, whether the role has
a display label, or which rows depend on a role rename. At that point the array
is hiding a missing child table.

Prefer a child table when the members are facts of their own:

```sql
CREATE TABLE app.user_role_grants (
    user_id bigint NOT NULL REFERENCES app.users(id),
    role_code text NOT NULL REFERENCES app.roles(code),
    granted_at timestamptz NOT NULL DEFAULT now(),
    revoked_at timestamptz,
    PRIMARY KEY (user_id, role_code, granted_at)
);
```

Use the Phase 4b lesson chain `arrays/what-arrays-are-good-for`,
`arrays/what-arrays-are-bad-for`, `arrays/querying-arrays`, and
`ranges-vs-arrays-vs-child-tables` to teach the distinction before later
decision-engine catalogs cite this page.

# Reference Solution

The modeled fact is not "a user has a small label set." The modeled fact is a
role grant with lifecycle. A role can be granted, revoked, audited, described,
renamed, and constrained. `roles text[]` hides those facts inside one value, so
revocation becomes array rewriting, audit has nowhere to live, and role
metadata must be duplicated or inferred in application code.

A better design separates role definitions from role grants:

```sql
CREATE TABLE app.roles (
    code text PRIMARY KEY,
    label text NOT NULL UNIQUE,
    description text NOT NULL DEFAULT ''
);

CREATE TABLE app.user_role_grants (
    user_id bigint NOT NULL REFERENCES app.users(id),
    role_code text NOT NULL REFERENCES app.roles(code),
    granted_at timestamptz NOT NULL DEFAULT now(),
    revoked_at timestamptz,
    granted_by bigint REFERENCES app.users(id),
    PRIMARY KEY (user_id, role_code, granted_at)
);
```

The migration shape is to create the child tables, backfill role codes from the
array, then stop writing the array:

```sql
INSERT INTO app.roles (code, label)
SELECT DISTINCT role_code, initcap(replace(role_code, '_', ' '))
FROM app.users
CROSS JOIN unnest(roles) AS role_code;

INSERT INTO app.user_role_grants (user_id, role_code)
SELECT id, role_code
FROM app.users
CROSS JOIN unnest(roles) AS role_code;
```

After the application reads and writes `user_role_grants`, drop `users.roles`.
An array was a bad fit because each element needed identity and history.

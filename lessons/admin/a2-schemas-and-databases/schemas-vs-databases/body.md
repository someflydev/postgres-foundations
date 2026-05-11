# Schemas vs Databases

## Problem Framing

Schemas vs Databases belongs in the administration track because it is one of the places where a correct PostgreSQL design becomes an operable PostgreSQL system. The learner has already seen phase 10 security and federation features. This lesson asks a different question: if a production saas database is running at 02:00, can an operator explain who can connect, what object names resolve to, which privileges are active, and what evidence proves the answer?

The concrete focus is this: The default advice is one database with many schemas for related application data; use separate databases when lifecycle, restore, locale, or isolation demands it. This is not a vocabulary exercise. A production incident usually arrives as a failed deploy, a leaked credential, an unexpected permission denied, a bad restore target, or a privileged function doing more than its author expected. The administrator needs a small set of exact PostgreSQL facts and a repeatable way to verify them.

## Minimal Concept Introduction

In module Schemas and databases, every decision should be described as actor, object, operation, and evidence. The actor might be a login role, a NOLOGIN group role, a migration owner, a schema owner, or the database owner. The object might be a database, schema, table, sequence, function, or catalog entry. The operation is specific: `CONNECT`, schema `USAGE`, schema `CREATE`, table `SELECT`, table `INSERT`, sequence `USAGE`, sequence `UPDATE`, function `EXECUTE`, `SET ROLE`, or `CREATE DATABASE`.

For this lesson, the important example is: keep `saas`, `reporting`, and `audit` schemas in one database so cross-schema transactions and backups stay coherent. The useful habit is to name the positive permission and the negative boundary. A runtime role may be allowed to read and write tenant-scoped business rows, but it should not own the schema, create arbitrary functions, change row-level-security policy definitions, or grant itself privileges. A schema may hold a coherent application namespace, but it is not an excuse to put unrelated lifecycle boundaries into one bucket.

## Worked Example

Use the saas domain as the running lab. Start by writing the smallest explicit SQL that represents the decision:

```sql
CREATE SCHEMA IF NOT EXISTS reporting AUTHORIZATION saas_migrations;
GRANT USAGE ON SCHEMA reporting TO saas_app_readonly;
```

After applying the change, verify it from the catalog rather than from memory. Use `pg_auth_members` for membership. Use `pg_namespace` with `aclexplode(nspacl)` for schema ACLs. Use `information_schema.table_privileges` for table grants when it answers the question cleanly. Use `pg_class` with `aclexplode(relacl)` for sequences when you need exact sequence ACL evidence. Use `pg_proc` with `aclexplode(proacl)` for function EXECUTE grants. These are the same patterns captured in `seed-data/packs/admin/access-review-queries.sql`.

The worked example is complete only when the review output can be interpreted by someone who did not write the original grant. If the output says `saas_app_readwrite` can update `saas.documents`, the operator should know which login roles inherit that group. If the output says `public` has only USAGE, the operator should know that low-privileged roles cannot create shim objects there. If a database was created with `template0`, UTF8 encoding, and explicit locale settings, the restore runbook should say why those choices were made.

## Diagnostic Questions

Which exact PostgreSQL object carries the boundary in this lesson? Is the boundary attached to a role, a schema, a database, a function definition, a default privilege rule, or object ownership? Does the decision affect current objects, future objects, session state, name resolution, or cluster-level behavior? Which catalog query proves the state after the change? If a login credential leaks, which group memberships become reachable? If a restore is needed, does this design make the restore smaller, larger, safer, or harder to verify?

When debugging, avoid broad fixes. Do not jump from one permission denied error to `GRANT ALL`. First identify the missing operation and object type. A table grant will not create schema visibility. A schema grant will not permit table reads. A future default privilege will not repair a table that already exists. A new database may create a lifecycle boundary that complicates backup, pooling, and migrations. A search_path setting may change what a privileged function actually touches.

## Common Pitfalls

The common pitfall for this lesson is creating a new database for every internal boundary and then discovering backups, migrations, and connection pools multiplied. It usually happens because the team fixes the symptom instead of preserving the model. PostgreSQL makes that easy: a superuser session can paper over most mistakes. The admin track deliberately resists that reflex. The better repair is to use the smallest statement that restores the intended contract and then show the catalog evidence.

The recurring repair pattern is: choose a database only when the operational boundary is worth separate connections, dumps, and restore posture. Pair the repair with a rollback statement or at least a review query. If the change grants access, know how to revoke it. If it moves data or objects, know how ownership and dependent objects are preserved. If it relies on session state, know whether `current_user`, `session_user`, or `search_path` will change during execution. If it relies on defaults, know whether the rule applies only to future objects.

## Explain It Back

Explain Schemas vs Databases by naming the operational contract. A strong answer says what PostgreSQL object is being controlled, why that object is the correct boundary, which SQL changes the state, which SQL proves the state, and what risk remains. In the saas domain, the answer should also name how the decision interacts with RLS from phase 10: RLS protects rows, but roles, schemas, functions, ownership, databases, and search_path decide who can reach the row-protected objects in the first place.

End with an access-review sentence. For example: "After this change, I would rerun the admin access-review queries and expect to see only the named group role on the relevant object, no direct one-off login-role grants, and no CREATE privilege in shared namespaces unless the runbook explicitly allows it." That sentence turns the lesson from theory into operations.

## References and Further Reading

- `docs/admin-track/README.md` for the administration track map.
- `docs/admin-track/a1-roles-playbook.md` for role and privilege review patterns.
- `docs/admin-track/a2-schemas-playbook.md` for schema, database, and search_path practices.
- `seed-data/packs/admin/access-review-queries.sql` for executable catalog review queries.

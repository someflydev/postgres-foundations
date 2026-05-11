# Default Privileges

## Problem Framing

Manual grants are easy to get right once and easy to forget on the next
migration. Default privileges solve the forward-looking part of that problem:
when a specific owner role creates future objects in a schema, PostgreSQL can
apply grants automatically. This is not a cleanup command for old objects. It
is a contract for future objects, and the contract is tied to the role that
creates them. In a small SaaS database, this prevents a release from adding a
new table that the app cannot read or an analyst should not see.

## Minimal Concept Introduction

`ALTER DEFAULT PRIVILEGES` changes the privileges applied to objects created
later by a role. The optional `FOR ROLE` clause identifies the creator role.
The optional `IN SCHEMA` clause narrows where the rule applies. Defaults can
apply to tables, sequences, functions, types, and schemas. Existing objects are
unchanged, so a migration often has two parts: grant on current objects, then
alter default privileges for future objects. The creator role matters. If
`owner_a` has default privileges but `owner_b` creates the next table, `owner_a`
rules do not apply.

## Worked Example

In the Phase 10 SaaS seed, `ALTER DEFAULT PRIVILEGES IN SCHEMA saas GRANT
SELECT ON TABLES TO saas_readonly` documents the intent that future SaaS tables
remain visible to the read-only role. A more production-shaped migration would
run as a stable owner role and write `ALTER DEFAULT PRIVILEGES FOR ROLE
saas_owner IN SCHEMA saas GRANT SELECT ON TABLES TO saas_readonly`. To prove the
rule, create a small throwaway table as the owner role, inspect
`information_schema.role_table_grants`, and drop the table. If the grant is
missing, check which role created the table before changing the default rule.

## Diagnostic Questions

Are you granting on existing objects or future objects? Which role will create
future objects in migrations? Is the schema specified, or will the rule apply
too broadly? Do future sequences need separate privileges? Are functions
covered, and should they be? Can you demonstrate the default by creating a new
object, rather than assuming the command affected existing tables?

## Common Pitfalls

The main pitfall is expecting default privileges to repair old objects. Another
is setting defaults as a personal login role while migrations run as a service
or owner role. A third is forgetting that sequences are separate object types.
Finally, broad default privileges can accidentally publish future tables before
the team has decided whether they are safe for reporting roles.

## Explain It Back

Explain default privileges as a release-safety mechanism. Name the creator
role, schema, object type, receiving role, and reason. A complete explanation
also states what remains outside the command: existing objects, objects created
by another owner, and object types not named in the statement. That boundary is
why default privileges belong in migration review rather than as an emergency
fix after a failed deployment.

## References and Further Reading

- `docs/authoring-exercises.md` for schema exercise expectations.
- `docs/rls-playbook.md` for pairing grants with tenant policies.

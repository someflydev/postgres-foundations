# Login vs Group Roles and Membership

## Problem Framing

PostgreSQL roles are the first access-control design surface learners meet in
Phase 10. A login role answers "who can connect?" A group role answers "what
capability does this actor receive after connecting?" Mixing those questions is
how a small lab turns into a production database where every user has hand-made
grants no one can audit. In the SaaS corpus, application sessions, reporting
users, migration operators, and table owners need different powers. The goal is
not to create a role for every noun in the business. The goal is to make access
reviewable: a few group roles carry privileges, and login roles receive
membership.

## Minimal Concept Introduction

`CREATE ROLE app_user LOGIN` creates an identity that can authenticate.
`CREATE ROLE saas_reader NOLOGIN` creates a group role that cannot connect by
itself. `GRANT saas_reader TO app_user` gives the login role membership in the
group role. PostgreSQL also supports role attributes such as `CREATEDB`,
`CREATEROLE`, `REPLICATION`, and `BYPASSRLS`; these are powerful and should be
rare. Membership can be inherited or require `SET ROLE`, depending on how the
role is created and used. In this course, start with inherited group roles for
ordinary application access and reserve elevated role attributes for explicit
operator workflows.

## Worked Example

For a tenant-scoped SaaS app, create `saas_app` as the normal application
capability and `saas_readonly` as a reporting capability. Grant schema usage to
both. Grant `SELECT, INSERT, UPDATE, DELETE` on tenant-owned tables to
`saas_app`; grant only `SELECT` to `saas_readonly`. Then create login roles such
as `app_pooler LOGIN` and `analyst_lee LOGIN`, and grant them membership in the
appropriate group roles. The login role can change over time without rewriting
table grants. To inspect the model, query `pg_roles`, `pg_auth_members`, and
`information_schema.role_table_grants`, then explain the answer in terms of
actors and capabilities.

## Diagnostic Questions

Which roles can authenticate? Which roles are only privilege bundles? Which role
owns the objects, and should application sessions ever use that owner role?
Does a migration need temporary elevated access, or should it run as a durable
owner role? Can a reviewer answer "who can read `saas.documents`?" without
opening every table definition? Are dangerous attributes such as `BYPASSRLS`,
`CREATEROLE`, or `REPLICATION` absent from ordinary application roles?

## Common Pitfalls

The most common mistake is granting directly to login roles. That works for one
person and fails once there are ten humans, a pooler, and a background worker.
Another mistake is using the table owner as the app role; owners bypass many
ordinary privilege checks and can surprise RLS tests unless `FORCE ROW LEVEL
SECURITY` is used. A third mistake is assuming `PUBLIC` is harmless. Revoking
unneeded public privileges is often part of a serious role review.

## Explain It Back

Explain the role model as a permission graph. Name the login roles, the group
roles, the memberships, and the objects each group role can touch. Then name
the role that should not be used by the application: the owner or migration
role. A good answer should make future changes boring. Adding a new analyst
should mean granting membership in `saas_readonly`, not repeating grants over
every schema, table, sequence, and function.

## References and Further Reading

- `docs/rls-playbook.md` for how roles interact with RLS policy testing.
- `docs/lab.md` for the Phase 10 lab environment.

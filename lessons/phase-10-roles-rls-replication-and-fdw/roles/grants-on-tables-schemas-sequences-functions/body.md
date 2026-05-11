# Grants on Tables Schemas Sequences Functions

## Problem Framing

PostgreSQL privileges are object-specific. A role can have `SELECT` on a table
and still fail because it lacks `USAGE` on the schema. A role can insert rows
and still fail because it cannot use the identity sequence. A role can call a
function that leaks more than the table grants would have allowed. This lesson
builds the habit of naming the object class before writing `GRANT`. In Phase
10, that matters because RLS and FDW do not replace privileges; they layer on
top of privileges.

## Minimal Concept Introduction

Schemas require `USAGE` before contained objects can be referenced. Tables have
privileges such as `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`,
`REFERENCES`, and `TRIGGER`. Sequences have `USAGE`, `SELECT`, and `UPDATE`.
Functions use `EXECUTE`. `GRANT` adds a privilege or membership; `REVOKE`
removes one. Grants can include `WITH GRANT OPTION`, but that should be rare in
a training lab and rarer in production. Always ask whether the role needs to
use a schema, read an object, change an object, or delegate access.

## Worked Example

Suppose `saas_app` must write documents. It needs `USAGE ON SCHEMA saas`, table
privileges on `saas.documents`, and sequence privileges for tables that use
standalone sequences. Because `saas.documents.id` uses a UUID default, there is
no document sequence. `saas.audit_events.id`, however, is an identity column
backed by a sequence, so an insert path may need sequence privileges depending
on ownership and grants. A practical review query checks
`information_schema.role_table_grants`, `information_schema.usage_privileges`,
and `pg_class` for sequences. The result should be a short matrix: role, object,
privilege, reason.

## Diagnostic Questions

Does the role have schema `USAGE`? Is the missing privilege on the table or on a
sequence? Is a function executable by `PUBLIC` when it should be restricted? Is
the role using a broad grant on every table because the author did not know
which table was needed? Does revoking a privilege break a real workflow or only
remove accidental access? Can the error message be mapped to a specific object
class?

## Common Pitfalls

Granting `ALL PRIVILEGES` is the fastest way to hide the real requirement.
Granting on existing tables but forgetting future tables causes migrations to
break later; that belongs to the default privileges lesson. Forgetting sequences
causes confusing insert failures. Treating function execution as harmless is
also risky: `SECURITY DEFINER` functions run with the definer's privileges and
need deliberate review.

## Explain It Back

Explain each grant with a sentence that names the role, object type, object
name, privilege, and workflow. For example: "`saas_app` receives `INSERT` on
`saas.audit_events` so the application can write append-only audit records after
setting `app.tenant_id`." If the sentence sounds vague, the grant is probably
too broad. Good grant design is not about writing less SQL; it is about making
the permission story easy to test and easy to revoke.

## References and Further Reading

- `docs/rls-playbook.md` for privilege and policy layering.
- `docs/learner-workflow.md` for lab reset and verification habits.

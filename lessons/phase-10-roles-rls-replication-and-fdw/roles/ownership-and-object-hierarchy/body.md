# Ownership and Object Hierarchy

## Problem Framing

Ownership is stronger than a grant. The owner of a table can alter or drop it,
grant privileges on it, and often bypass the ordinary permission story learners
are trying to test. That is why application roles should usually not own the
objects they use. Ownership also explains why moving one table is not enough:
schemas, tables, sequences, views, functions, publications, and foreign servers
all have owners. Phase 10 asks learners to separate three jobs: owning objects,
using objects, and administering exceptional workflows.

## Minimal Concept Introduction

Every PostgreSQL object has an owner. `ALTER ... OWNER TO ...` changes that
owner for many object types. Ownership is not inherited from schema ownership
after object creation; owning a schema does not mean owning every table inside
it. Dropping or changing ownership can be blocked by dependent objects. Views
and functions add another layer because they can execute with invoker or
definer privileges. Publications, subscriptions, and foreign servers introduce
operational ownership that should not be casually assigned to application
roles.

## Worked Example

Create a durable owner role such as `saas_owner NOLOGIN`. Tables in `saas`
belong to that owner. The application role receives grants but does not own the
tables. Analysts receive read-only membership. If an application session tries
to alter `saas.documents`, it should fail. If a migration needs to change the
table, it should run as the owner or through a controlled migration path. To
review a database, query `pg_class`, `pg_namespace`, `pg_proc`, and
`pg_foreign_server` for owner OIDs joined to `pg_roles`. Then look for any
object owned by a login role or by the same role used for normal app traffic.

## Diagnostic Questions

Which role owns the schema? Which role owns the tables? Who owns sequences that
support identity columns? Are functions owned by a role that can read data the
caller should not read? Does the application role own any object it should only
use? If a role is dropped, which objects block the drop? Is `REASSIGN OWNED`
needed during operator offboarding?

## Common Pitfalls

Using the superuser or app login for migrations makes later access reviews
muddy. Changing a table owner but forgetting related sequences can produce odd
failures. Assuming schema ownership grants table access also leads to confusion.
Finally, `SECURITY DEFINER` functions can unintentionally turn ownership into a
privilege escalation path if the function body and search path are not reviewed.

## Explain It Back

Explain ownership as custody, not usage. The owner can reshape the object; the
grantee can perform named actions. A good design has a boring owner role, a few
usage roles, and login roles that receive membership. When learners can point
to an object and say "owned by migration role, used by application role,
observed by reporting role," they are ready to combine ownership with RLS and
replication boundaries.

## References and Further Reading

- `docs/rls-playbook.md` for owner bypass and `FORCE ROW LEVEL SECURITY`.
- `docs/lab.md` for the Phase 10 seed roles.

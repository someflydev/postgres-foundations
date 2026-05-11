# Modernization Bridge Narrative

You are advising a product team inside a company with a legacy monolith
database. The old database contains customers, orders, and products in a shape
that predates current modeling discipline. The organization wants a new service,
but it does not yet have buy-in for a full migration or rewrite. The team still
has to ship. It needs accurate reads against selected legacy data, local writes
with strict correctness, and a credible plan for eventual migration.

The lab models this with two PostgreSQL 16 databases. The "new" database uses
`postgres_fdw` to see selected legacy tables on the other database. In the real
world the boundary might involve network latency, legacy ownership politics,
different release calendars, and missing tenant isolation. In the capstone the
same concerns are represented through foreign tables, local mapping tables,
materialized aggregate caches, and RLS on the new-service side.

The key design question is ownership. The legacy database remains the source of
truth for legacy customers, orders, and products. The new service owns only its
local tables: tenant records, customer links, local orders, entitlements, audit
state, and any materialized caches it refreshes. It must not pretend that a
foreign table is as cheap or as controllable as a local table. It must also not
push new-service writes back into the monolith without a migration contract.

The capstone requires `postgres_fdw`, `IMPORT FOREIGN SCHEMA`, and at least one
materialized view that caches an aggregate from the legacy side. That cache must
come with a refresh policy and a staleness statement. A careless refresh policy
can make the new service present stale totals while direct FDW reads show the
newer truth. The included concurrency scenario exists to make that critique
concrete.

Logical replication is intentionally discussed but not implemented. It becomes
the next move when the organization is ready to move ownership incrementally,
when identifiers and conflict rules are settled, and when the team can operate
publication/subscription lag, slot growth, backfills, and cutover. Citus is also
not part of the answer. This is not yet a distributed data problem; it is an
ownership, correctness, and migration-sequencing problem.

Your answer should be practical. Build the bridge that can ship without hiding
the cost of the bridge. Name what breaks when FDW is slow or unavailable. Name
what RLS does and does not protect. Name when the materialized view can be
stale. Then describe the evidence that would justify promoting the bridge into
an incremental logical-replication migration.

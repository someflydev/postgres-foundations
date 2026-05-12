# E6 postgres_fdw Deep

postgres_fdw is a federation tool, not a permanent substitute for ownership.
Phase 10 introduced the bridge pattern; E6 goes deeper into predicate pushdown,
join and aggregate pushdown, async append, foreign-table statistics,
authentication, SSL, and reliability behavior when the remote server is slow or
unavailable.

Use `EXPLAIN (VERBOSE)` as the primary proof. A good FDW answer shows which
filters, joins, or aggregates are sent as remote SQL and which work is still
performed locally. When pushdown fails, prefer rewrites that preserve semantics
and keep non-pushable functions away from the remote filter or aggregate path.

The production decision should also name the exit strategy. Federation may be a
temporary modernization bridge, a deliberate boundary between systems, or a sign
that logical replication and consolidation would be more reliable than another
remote query path.

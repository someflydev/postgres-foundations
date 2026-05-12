# Modernization Bridge with Extension Decisions

A team is replacing pieces of a legacy monolith with a PostgreSQL service. The service needs its own local schema, search over new records, safe reads from the legacy database through postgres_fdw, and logical replication to a BI replica.

A team member has proposed Citus. Your job is to decide whether that proposal belongs now, later, or should be avoided for this workload, while still delivering the bridge.

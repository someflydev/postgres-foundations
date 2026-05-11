# Modernization Bridge Brief

Design a new PostgreSQL 16 service that reads selected customer, order, and
product data from a legacy PostgreSQL 16 database through `postgres_fdw`. The
new service must write its own local state correctly and enforce tenant
isolation with RLS even though the legacy database has no tenant-aware RLS.

Use `postgres_fdw`, `IMPORT FOREIGN SCHEMA`, and at least one materialized view
that caches an aggregate from the legacy side. Define the refresh policy and
state the acceptable staleness. Include at least eight critical queries, with
several crossing the FDW boundary or relying on the materialized aggregate.

Discuss logical replication, but do not implement it. Your writeup must say
when logical replication becomes the right next move for migration. Also explain
why Citus is not appropriate now. The extension posture must list what is
enabled now, what is deferred, and the measured or organizational signals that
would change the answer.

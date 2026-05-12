-- One acceptable answer for ltree-what-ltree-is-for-level-a-2.
-- Use ltree evidence for materialized-path hierarchies for category trees, org charts, and nested comment threads. Name the core PostgreSQL alternative, the missing workload signal, the verification step, and the not-yet boundary.
CREATE EXTENSION IF NOT EXISTS ltree;
SELECT 'Top.Electronics.Cameras'::ltree @> 'Top.Electronics.Cameras.Lenses'::ltree AS is_ancestor;

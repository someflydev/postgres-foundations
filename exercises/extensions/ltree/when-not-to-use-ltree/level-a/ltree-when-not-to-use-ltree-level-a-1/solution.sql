-- One acceptable answer for ltree-when-not-to-use-ltree-level-a-1.
-- Use ltree evidence for why most hierarchies are not deep enough to justify a specialized path type. Name the core PostgreSQL alternative, the missing workload signal, the verification step, and the not-yet boundary.
CREATE EXTENSION IF NOT EXISTS ltree;
SELECT 'Top.Electronics.Cameras'::ltree @> 'Top.Electronics.Cameras.Lenses'::ltree AS is_ancestor;

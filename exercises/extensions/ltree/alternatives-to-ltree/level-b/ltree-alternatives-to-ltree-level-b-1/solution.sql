-- One acceptable answer for ltree-alternatives-to-ltree-level-b-1.
-- Use ltree evidence for recursive CTE adjacency lists, closure tables, and the narrow cases where ltree wins. Name the core PostgreSQL alternative, the missing workload signal, the verification step, and the not-yet boundary.
CREATE EXTENSION IF NOT EXISTS ltree;
SELECT 'Top.Electronics.Cameras'::ltree @> 'Top.Electronics.Cameras.Lenses'::ltree AS is_ancestor;

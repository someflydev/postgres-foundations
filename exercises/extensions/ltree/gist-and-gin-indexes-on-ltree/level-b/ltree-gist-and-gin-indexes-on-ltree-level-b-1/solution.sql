-- One acceptable answer for ltree-gist-and-gin-indexes-on-ltree-level-b-1.
-- Use ltree evidence for GiST and GIN index choices for ltree containment and query patterns. Name the core PostgreSQL alternative, the missing workload signal, the verification step, and the not-yet boundary.
CREATE EXTENSION IF NOT EXISTS ltree;
SELECT 'Top.Electronics.Cameras'::ltree @> 'Top.Electronics.Cameras.Lenses'::ltree AS is_ancestor;

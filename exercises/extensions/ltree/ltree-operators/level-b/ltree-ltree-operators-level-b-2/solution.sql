-- One acceptable answer for ltree-ltree-operators-level-b-2.
-- Use ltree evidence for operators such as ~, @>, <@, lquery, and ltxtquery. Name the core PostgreSQL alternative, the missing workload signal, the verification step, and the not-yet boundary.
CREATE EXTENSION IF NOT EXISTS ltree;
SELECT 'Top.Electronics.Cameras'::ltree @> 'Top.Electronics.Cameras.Lenses'::ltree AS is_ancestor;

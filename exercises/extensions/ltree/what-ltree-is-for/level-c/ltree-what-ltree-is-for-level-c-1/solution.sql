-- One acceptable answer for ltree-what-ltree-is-for-level-c-1.
-- Build a categories tree for ecommerce products with ltree paths, then query ancestors and descendants with @>, <@, lquery, and an indexed path lookup.
CREATE EXTENSION IF NOT EXISTS ltree;
SELECT 'Top.Electronics.Cameras'::ltree @> 'Top.Electronics.Cameras.Lenses'::ltree AS is_ancestor;

# Extension Catalog Sync

`decision-engine/catalogs/extensions.json` uses `module_slug` to connect each
extension recommendation to the curriculum module or lesson that teaches the
capability.

For extension-track modules, `module_slug` must match the canonical module IDs
in `curriculum/extensions/map.json`, such as `e1-pg-stat-statements`,
`e2-pg-trgm`, `e3-postgis`, `e4-pgvector`, `e5-timescaledb`,
`e6-postgres-fdw`, `e7-citus`, `ltree`, `pg-partman`, and `pgbouncer`.
Core-contrib helpers that are taught inside phase lessons may point at the
slug-aligned lesson ID instead.

`uv run pgfound decision catalog check` validates these links, along with
extension anti-pattern references and anti-pattern documentation paths.
The extension schema also requires `not_yet_triggers` so rule authors have
concrete reasons to defer an extension instead of turning every workload signal
into an immediate recommendation.

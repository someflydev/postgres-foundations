# ltree

ltree stores materialized paths for hierarchical data. It is useful for deep and frequently queried category trees, org charts, nested comments, and other hierarchies where ancestor and descendant predicates are central.

Compare it with adjacency lists, recursive CTEs, and closure tables before adopting it. Most shallow hierarchies do not need a specialized path type. Use GiST or GIN indexes based on the operator mix and verify with representative ancestor, descendant, and pattern queries.

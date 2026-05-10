WITH RECURSIVE category_tree AS (
    SELECT id, parent_id, name, 1 AS depth, name::text AS path
    FROM ecommerce.categories
    WHERE parent_id IS NULL
    UNION ALL
    SELECT child.id, child.parent_id, child.name, parent.depth + 1, parent.path || ' > ' || child.name
    FROM ecommerce.categories child
    JOIN category_tree parent ON parent.id = child.parent_id
)
SELECT path, depth
FROM category_tree
ORDER BY path;

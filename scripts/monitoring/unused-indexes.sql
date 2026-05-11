-- Purpose: find non-constraint indexes with no recorded scans as candidates for review, not automatic drop.
-- Reset statistics, rare reports, and rollback plans must be considered before dropping.
SELECT
    schemaname,
    relname AS table_name,
    indexrelname AS index_name,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND NOT EXISTS (
      SELECT 1
      FROM pg_constraint c
      WHERE c.conindid = pg_stat_user_indexes.indexrelid
  )
ORDER BY pg_relation_size(indexrelid) DESC, schemaname, relname, indexrelname
LIMIT 25;

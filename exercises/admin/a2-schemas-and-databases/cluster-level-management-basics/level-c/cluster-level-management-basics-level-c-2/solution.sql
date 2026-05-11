-- Cluster Level Management Basics Level C2
-- Repair goal: reserve new databases for real lifecycle boundaries and document template, encoding, and locale choices.
CREATE DATABASE restore_drill
  WITH TEMPLATE template0
  ENCODING 'UTF8'
  LC_COLLATE 'C.UTF-8'
  LC_CTYPE 'C.UTF-8';
-- Review evidence should be captured from seed-data/packs/admin/access-review-queries.sql.

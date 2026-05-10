CREATE EXTENSION IF NOT EXISTS btree_gist;
DROP TABLE IF EXISTS pgfound.phase4b_overlap_demo;
CREATE TABLE pgfound.phase4b_overlap_demo (
    professional_id bigint NOT NULL,
    slot tstzrange NOT NULL,
    EXCLUDE USING gist (professional_id WITH =, slot WITH &&)
);
INSERT INTO pgfound.phase4b_overlap_demo VALUES
    (1, tstzrange('2026-02-10 15:00+00', '2026-02-10 16:00+00', '[)'));
DO $$
BEGIN
    INSERT INTO pgfound.phase4b_overlap_demo VALUES
        (1, tstzrange('2026-02-10 15:30+00', '2026-02-10 16:30+00', '[)'));
EXCEPTION
    WHEN exclusion_violation THEN
        RAISE NOTICE 'conflicting key value rejected';
END
$$;
SELECT 'conflicting key value rejected' AS proof;

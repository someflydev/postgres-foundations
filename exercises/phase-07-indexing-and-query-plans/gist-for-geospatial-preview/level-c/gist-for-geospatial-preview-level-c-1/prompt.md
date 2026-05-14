# GiST for Geospatial Preview Level C1

## Scenario

The logistics PostGIS profile has service-zone polygons and delivery-event points.

## Task

Run the before query, make the smallest defensible change, run ANALYZE when statistics can change, and capture the after plan. Defend whether this belongs in the PostGIS profile now or remains a not-yet boundary with GiST-backed spatial predicates such as ST_Contains and ST_DWithin with correct SRID handling.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.

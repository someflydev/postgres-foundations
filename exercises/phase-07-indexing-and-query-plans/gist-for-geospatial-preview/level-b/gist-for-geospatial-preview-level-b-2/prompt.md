# GiST for Geospatial Preview Level B2

## Scenario

The logistics PostGIS profile has service-zone polygons and delivery-event points.

## Task

Compare two candidate access paths or rewrites. Use row estimates, actual rows, buffers, and maintenance cost to decide whether this belongs in the PostGIS profile now or remains a not-yet boundary. Include GiST-backed spatial predicates such as ST_Contains and ST_DWithin with correct SRID handling.

## Required Artifact

Submit the relevant SQL or critique notes plus the before/after plan observations. Name the read benefit, write or storage cost, and the condition that would make you remove or defer the index.

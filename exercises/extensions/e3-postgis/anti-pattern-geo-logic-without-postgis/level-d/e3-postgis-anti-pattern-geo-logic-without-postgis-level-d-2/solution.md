# Solution

Replace the DIY Haversine filter with typed PostGIS data, a GiST index, and `ST_DWithin`. The original query can be acceptable for a tiny table, but it forces a sequential scan at scale and hides SRID assumptions. Store a `geography(Point,4326)` or a generated geography column, index it, and compare EXPLAIN output before and after.

# Geo Logic without PostGIS

The anti-pattern is storing coordinates as arrays or separate floats, then rebuilding spatial behavior with ad hoc Haversine expressions, bounding boxes, or application loops. This can work for a small demo, but it hides SRID assumptions, blocks useful spatial indexes, and usually becomes a sequential scan when data volume grows.

Use core PostgreSQL for ordinary numeric storage when coordinates are only displayed or passed to another system. Use PostGIS when the database owns spatial predicates such as containment, intersection, distance-bounded search, or coordinate transforms. The decision point is not the presence of latitude and longitude; it is whether spatial correctness and planner support are part of the workload.

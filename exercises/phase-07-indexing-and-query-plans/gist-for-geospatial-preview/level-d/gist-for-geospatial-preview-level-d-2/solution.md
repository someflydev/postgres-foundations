# Solution Notes

This is a PostGIS-profile exercise, not a core-only range GiST drill. A strong answer names the spatial predicate, the type, and the SRID. `ST_Contains(z.geom, e.geom)` uses geometry service-zone polygons and event points. `ST_DWithin(...::geography, 5000)` is the distance-bounded form when meters over the earth's surface matter.

The defensible index is a GiST index on the spatial column, for example:

```sql
CREATE INDEX service_zones_geom_gist_idx
ON logistics.service_zones USING gist (geom);

CREATE INDEX delivery_events_geog_gist_idx
ON logistics.delivery_events USING gist (geog);
```

Do not accept application-side latitude and longitude math as equivalent evidence. The operational defense should also state when PostGIS is not yet justified: display-only coordinates, tiny tables, unsupported managed-service posture, or no hot containment/distance predicate.

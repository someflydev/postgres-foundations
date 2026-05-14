# GiST for Geospatial Preview

## Problem Framing

This lesson is a preview, not a full PostGIS module. Phase 7b is still teaching access-path reasoning, but real geospatial indexing is one of the clearest reasons GiST exists. Latitude and longitude columns can be enough for display. They are not enough for reliable containment, distance, SRID handling, or spatial indexing. When the workload asks "which deliveries are inside this service zone?" or "which points are within five kilometers?" the design has crossed from scalar columns into spatial predicates.

The core-first doctrine still applies. Do not enable PostGIS because a table has coordinates. Enable it when geometry or geography is a real part of the workload and the operational environment can support the extension. This preview uses the `logistics_geo` seed pack and the PostGIS profile as a boundary: the main Phase 7 lab can discuss the plan shape, while executable spatial drills belong in the PostGIS-capable lab.

## Minimal Concept Introduction

PostGIS adds `geometry` and `geography` types, SRID-aware constructors, spatial functions such as `ST_Contains` and `ST_DWithin`, and GiST operator classes for spatial indexes. GiST stores bounding boxes and related search-tree information so PostgreSQL can eliminate shapes that cannot match before it performs exact spatial checks. The index is not the entire answer. The query still needs correct SRID, the right type, and functions that can use the index.

`geometry` is usually appropriate for planar calculations in a known projection or for many containment checks. `geography` is useful for distance over the earth's surface, with different cost and behavior. A learner should not blur those types. Choosing between them is part of the design.

## Worked Example

Worked example anchor: service-zone-point-containment

A logistics team needs to find delivery events inside service-zone polygons:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT e.id, e.event_name, z.zone_code
FROM logistics.delivery_events AS e
JOIN logistics.service_zones AS z
  ON ST_Contains(z.geom, e.geom)
WHERE z.zone_code = 'chi-loop';
```

The supporting index is spatial, not a B-tree on latitude:

```sql
CREATE INDEX service_zones_geom_gist_idx
ON logistics.service_zones USING gist (geom);

CREATE INDEX delivery_events_geom_gist_idx
ON logistics.delivery_events USING gist (geom);
ANALYZE logistics.service_zones;
ANALYZE logistics.delivery_events;
```

For nearby-driver style queries, the distance predicate should be explicit:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, event_name
FROM logistics.delivery_events
WHERE ST_DWithin(
    geog,
    ST_SetSRID(ST_MakePoint(-87.6298, 41.8781), 4326)::geography,
    5000
);
```

This example names the SRID, uses `geography` for meter-based distance, and gives the planner a spatial predicate that can work with a GiST index. It is very different from computing distance in application code after fetching every point.

## Diagnostic Questions

Ask whether the workload needs display coordinates, containment, intersection, nearest-neighbor search, or distance thresholds. Ask whether the data uses a consistent SRID. Ask whether `geometry` or `geography` matches the business question. Ask whether the managed service supports the needed PostGIS version. Ask how large the spatial tables are, how often shapes change, and whether exact spatial checks dominate after the bounding-box index narrows candidates.

Also ask whether the Phase 7 core lab is the right place to run the query. Without the PostGIS profile, this remains a documented boundary and a plan-reading exercise. With the PostGIS profile, it becomes an executable spatial indexing drill.

## Common Pitfalls

The common failure is storing latitude and longitude as independent numeric columns and then writing homegrown distance or polygon logic. That can be wrong near boundaries and usually cannot use spatial indexes. Another pitfall is mixing SRIDs or casting between geometry and geography without knowing why. A third is assuming GiST removes all CPU cost; spatial indexes often produce candidates that still need exact function checks. A fourth is enabling PostGIS for display-only maps where a simple point column and application rendering would be enough.

## Explain It Back

A strong explanation says: "This is a geospatial workload because the query asks for containment and distance, not just display coordinates. PostGIS provides `geometry`, `geography`, SRID handling, `ST_Contains`, and `ST_DWithin`. GiST helps by narrowing candidate shapes or points before exact spatial checks. I would keep PostGIS out of the core lab unless those predicates are hot and the deployment environment supports the extension." That is the preview boundary this lesson is meant to teach.

## References and Further Reading

Use `docs/extension-track/e3-postgis.md` for the full extension posture and `seed-data/packs/logistics_geo/README.md` for the PostGIS seed pack used by executable spatial drills.

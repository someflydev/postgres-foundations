# logistics_geo

Small PostGIS seed pack for extension-track labs. Service-zone polygons are checked in as GeoJSON and loaded with `ST_GeomFromGeoJSON`; delivery events are generated as points inside or near those zones.

-- domain: logistics_geo
-- phase: 01
-- description: PostGIS service-zone polygons and delivery event points

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE SCHEMA IF NOT EXISTS logistics;

CREATE TABLE IF NOT EXISTS logistics.service_zones (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    zone_code text NOT NULL UNIQUE,
    zone_name text NOT NULL,
    geom geometry(Polygon, 4326) NOT NULL,
    geog geography(Polygon, 4326) GENERATED ALWAYS AS (geom::geography) STORED
);

CREATE TABLE IF NOT EXISTS logistics.delivery_events (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_name text NOT NULL,
    occurred_at timestamptz NOT NULL,
    geom geometry(Point, 4326) NOT NULL,
    geog geography(Point, 4326) GENERATED ALWAYS AS (geom::geography) STORED
);

WITH raw(feature) AS (
    SELECT jsonb_array_elements($geojson$
{
  "type": "FeatureCollection",
  "features": [
    {"type": "Feature", "properties": {"zone_code": "chi-loop", "zone_name": "Chicago Loop"}, "geometry": {"type": "Polygon", "coordinates": [[[-87.645,41.872],[-87.610,41.872],[-87.610,41.895],[-87.645,41.895],[-87.645,41.872]]]}},
    {"type": "Feature", "properties": {"zone_code": "nyc-midtown", "zone_name": "NYC Midtown"}, "geometry": {"type": "Polygon", "coordinates": [[[-73.995,40.744],[-73.955,40.744],[-73.955,40.770],[-73.995,40.770],[-73.995,40.744]]]}},
    {"type": "Feature", "properties": {"zone_code": "sf-soma", "zone_name": "San Francisco SoMa"}, "geometry": {"type": "Polygon", "coordinates": [[[-122.415,37.772],[-122.390,37.772],[-122.390,37.790],[-122.415,37.790],[-122.415,37.772]]]}}
  ]
}
$geojson$::jsonb -> 'features')
)
INSERT INTO logistics.service_zones (zone_code, zone_name, geom)
SELECT
    feature #>> '{properties,zone_code}',
    feature #>> '{properties,zone_name}',
    ST_SetSRID(ST_GeomFromGeoJSON((feature -> 'geometry')::text), 4326)
FROM raw
ON CONFLICT (zone_code) DO UPDATE
SET zone_name = EXCLUDED.zone_name, geom = EXCLUDED.geom;

INSERT INTO logistics.delivery_events (event_name, occurred_at, geom)
SELECT
    'delivery event ' || series.n,
    '2026-04-01 08:00:00+00'::timestamptz + (series.n * interval '15 minutes'),
    ST_SetSRID(ST_MakePoint(
        CASE ((series.n - 1) % 3)
            WHEN 0 THEN -87.640 + ((series.n % 20) * 0.0012)
            WHEN 1 THEN -73.990 + ((series.n % 20) * 0.0014)
            ELSE -122.412 + ((series.n % 20) * 0.0010)
        END,
        CASE ((series.n - 1) % 3)
            WHEN 0 THEN 41.875 + ((series.n % 12) * 0.0012)
            WHEN 1 THEN 40.747 + ((series.n % 12) * 0.0014)
            ELSE 37.775 + ((series.n % 12) * 0.0010)
        END
    ), 4326)
FROM generate_series(1, 720) AS series(n)
ON CONFLICT DO NOTHING;

CREATE INDEX IF NOT EXISTS service_zones_geom_gist_idx ON logistics.service_zones USING gist (geom);
CREATE INDEX IF NOT EXISTS delivery_events_geom_gist_idx ON logistics.delivery_events USING gist (geom);
CREATE INDEX IF NOT EXISTS delivery_events_geog_gist_idx ON logistics.delivery_events USING gist (geog);

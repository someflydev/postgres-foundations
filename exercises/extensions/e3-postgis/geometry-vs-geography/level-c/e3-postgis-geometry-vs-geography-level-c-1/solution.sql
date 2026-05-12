SELECT zone_name
FROM logistics.service_zones
WHERE ST_DWithin(geog, ST_SetSRID(ST_MakePoint(-87.6298, 41.8781), 4326)::geography, 5000)
ORDER BY zone_name;

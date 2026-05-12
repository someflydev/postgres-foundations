ALTER TABLE logistics.deliveries ENABLE ROW LEVEL SECURITY;
CREATE POLICY deliveries_region_policy ON logistics.deliveries
    USING (region_id = current_setting('app.region_id', true));

ALTER TABLE logistics.couriers ENABLE ROW LEVEL SECURITY;
CREATE POLICY couriers_region_policy ON logistics.couriers
    USING (region_id = current_setting('app.region_id', true));

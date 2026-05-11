ALTER TABLE device_fleets ENABLE ROW LEVEL SECURITY;
ALTER TABLE devices ENABLE ROW LEVEL SECURITY;
ALTER TABLE anomaly_notes ENABLE ROW LEVEL SECURITY;

CREATE POLICY device_fleets_account_read ON device_fleets
    USING (account_id::text = current_setting('app.account_id', true));

CREATE POLICY devices_account_read ON devices
    USING (
        EXISTS (
            SELECT 1
            FROM device_fleets f
            WHERE f.id = devices.fleet_id
              AND f.account_id::text = current_setting('app.account_id', true)
        )
    );

CREATE POLICY anomaly_notes_account_read ON anomaly_notes
    USING (
        EXISTS (
            SELECT 1
            FROM devices d
            JOIN device_fleets f ON f.id = d.fleet_id
            WHERE d.id = anomaly_notes.device_id
              AND f.account_id::text = current_setting('app.account_id', true)
        )
    );

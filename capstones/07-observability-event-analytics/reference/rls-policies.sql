ALTER TABLE observability.events ENABLE ROW LEVEL SECURITY;
CREATE POLICY events_service_owner_policy ON observability.events
    USING (service_name = current_setting('app.service_name', true) OR current_setting('app.service_name', true) = 'platform');

ALTER TABLE knowledge.documents ENABLE ROW LEVEL SECURITY;
CREATE POLICY documents_team_policy ON knowledge.documents
    USING (team_slug = current_setting('app.team_slug', true) OR current_setting('app.team_slug', true) = 'platform');

-- Q1 dashboard account summary.
CREATE INDEX accounts_tenant_status_updated_idx ON accounts (tenant_id, status, updated_at DESC);

-- Q2 pipeline by stage and Q6 deal detail lookup.
CREATE INDEX deals_tenant_stage_opened_idx ON deals (tenant_id, stage, opened_at DESC) WHERE closed_at IS NULL;
CREATE INDEX deals_tenant_account_idx ON deals (tenant_id, account_id);

-- Q3 recently touched contacts.
CREATE INDEX contacts_tenant_updated_idx ON contacts (tenant_id, updated_at DESC);

-- Q4 upcoming activities by assignee.
CREATE INDEX activities_tenant_assignee_due_idx
    ON activities (tenant_id, assigned_user_id, due_at)
    WHERE completed_at IS NULL;

-- Q5 tenant-scoped note search.
CREATE INDEX notes_tenant_created_idx ON notes (tenant_id, created_at DESC);
CREATE INDEX notes_search_vector_idx ON notes USING gin (search_vector);

-- Q7 bounded custom-field filter for a documented customer tier key.
CREATE INDEX accounts_custom_fields_gin_idx ON accounts USING gin (custom_fields jsonb_path_ops);

-- Q8 and Q10 audit review and retention candidates.
CREATE INDEX audit_events_tenant_occurred_idx ON audit_events (tenant_id, occurred_at DESC);
CREATE INDEX audit_events_occurred_idx ON audit_events (occurred_at);

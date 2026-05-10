CREATE TABLE pgfound.user_role_grants (user_id bigint NOT NULL, role_code text NOT NULL, granted_at timestamptz NOT NULL DEFAULT now());

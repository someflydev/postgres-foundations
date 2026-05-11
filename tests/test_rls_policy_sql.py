from __future__ import annotations

import re

from pgfound import paths


def test_phase10_rls_enabled_tables_have_policies() -> None:
    sql = (paths.SEED_DATA_DIR / "packs/saas_multi_tenant/phases/phase-10.sql").read_text(
        encoding="utf-8"
    )

    enabled_tables = set(
        re.findall(
            r"ALTER\s+TABLE\s+(?P<table>[a-z_]+\.[a-z_]+)\s+ENABLE\s+ROW\s+LEVEL\s+SECURITY",
            sql,
            flags=re.IGNORECASE,
        )
    )
    policy_tables = set(
        re.findall(
            r"CREATE\s+POLICY\s+[a-z_]+\s+ON\s+(?P<table>[a-z_]+\.[a-z_]+)",
            sql,
            flags=re.IGNORECASE,
        )
    )

    assert enabled_tables == {"saas.documents", "saas.audit_events"}
    assert enabled_tables <= policy_tables
    assert "WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid)" in sql

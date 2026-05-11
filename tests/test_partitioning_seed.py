from __future__ import annotations

import os
import subprocess
import sys

import pytest

from pgfound import paths
from pgfound.content import seed as content_seed


def test_phase9_partition_manifest_generator_is_deterministic() -> None:
    generator = paths.SEED_DATA_DIR / "packs/event_heavy_ops/generators/phase_09.py"

    first = subprocess.run([sys.executable, str(generator)], check=True, capture_output=True)
    second = subprocess.run([sys.executable, str(generator)], check=True, capture_output=True)

    assert first.stdout == second.stdout
    manifest = (
        paths.REPO_ROOT / "tmp/generated-seed-data/event_heavy_ops/phase-09/partition_manifest.csv"
    )
    text = manifest.read_text(encoding="utf-8")
    assert "event_log_partitioned_2025_05" in text
    assert "detached-cold" in text


def test_phase9_seed_sql_has_idempotent_drop_and_partition_contracts() -> None:
    event_sql = (paths.SEED_DATA_DIR / "packs/event_heavy_ops/phases/phase-09.sql").read_text(
        encoding="utf-8"
    )
    ecommerce_sql = (paths.SEED_DATA_DIR / "packs/ecommerce/phases/phase-09.sql").read_text(
        encoding="utf-8"
    )

    assert "DROP TABLE IF EXISTS events.event_log_partitioned CASCADE" in event_sql
    assert "DROP TABLE IF EXISTS ecommerce.orders_partitioned CASCADE" in ecommerce_sql
    assert "event_uuid, event_time" in event_sql
    assert "order_number, ordered_at" in ecommerce_sql
    assert "events.event_log_cold_2025_05" in event_sql


@pytest.mark.skipif(
    os.environ.get("PGFOUND_RUN_DB_TESTS") != "1",
    reason="set PGFOUND_RUN_DB_TESTS=1 to run the live Phase 9 seed idempotence smoke",
)
def test_phase9_event_seed_can_apply_twice_against_live_lab() -> None:
    plan = content_seed.plan_seed("event_heavy_ops", phase="9")

    content_seed.execute_seed(plan, reset=True, generate=True)
    content_seed.execute_seed(plan, reset=False, generate=True)

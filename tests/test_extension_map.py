from __future__ import annotations

import json

from pgfound import paths
from pgfound.content import validate

EXTENSION_MODULES = [
    "e1-pg-stat-statements",
    "e2-pg-trgm",
    "e3-postgis",
    "e4-pgvector",
    "e5-timescaledb",
    "e6-postgres-fdw",
    "e7-pg-cron",
    "ltree",
    "pg-partman",
    "pgbouncer",
]


def test_extension_map_validates_and_lists_canonical_modules() -> None:
    report = validate.validate_content(path_globs=("curriculum/extensions/map.json",))
    assert report.ok, [issue.message for issue in report.errors]

    data = json.loads(
        (paths.CURRICULUM_DIR / "extensions" / "map.json").read_text(encoding="utf-8")
    )
    assert [module["id"] for module in data["modules"]] == EXTENSION_MODULES
    assert {module["capability_layer"] for module in data["modules"]} == {"extension_mastery"}
    assert data["modules"][0]["prerequisites"] == [
        {"phase": 7},
        {"admin_module": "a5-monitoring-and-performance-ops"},
    ]

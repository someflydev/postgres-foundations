from __future__ import annotations

import json

from pgfound import paths
from pgfound.content import validate

ADMIN_MODULES = [
    "a1-roles-and-privileges",
    "a2-schemas-and-databases",
    "a3-auth-and-pooling",
    "a4-maintenance-and-lifecycle",
    "a5-monitoring-and-performance-ops",
    "a6-replication-and-ha",
]


def test_admin_map_validates_and_lists_a1_to_a6() -> None:
    report = validate.validate_content(path_globs=("curriculum/admin/map.json",))
    assert report.ok, [issue.message for issue in report.errors]

    data = json.loads((paths.CURRICULUM_DIR / "admin" / "map.json").read_text(encoding="utf-8"))
    assert [module["id"] for module in data["modules"]] == ADMIN_MODULES
    assert {module["capability_layer"] for module in data["modules"]} == {"admin_mastery"}
    assert all(module["prerequisites"] == [{"phase": 10}] for module in data["modules"])

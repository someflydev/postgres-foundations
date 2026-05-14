from __future__ import annotations

import json
from pathlib import Path

from pgfound import paths

CORE_CAPSTONE_IDS = (
    "01-multi-tenant-saas-crm",
    "02-scheduling-availability",
    "03-event-heavy-ops",
    "04-modernization-bridge",
)

EXTENSION_CAPSTONE_IDS = (
    "05-geo-logistics-platform",
    "06-ai-knowledge-platform",
    "07-observability-event-analytics",
    "08-modernization-bridge-extensions",
)

ALL_CAPSTONE_IDS = CORE_CAPSTONE_IDS + EXTENSION_CAPSTONE_IDS


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def industry_scenario_dirs() -> list[Path]:
    return sorted(
        path.parent for path in (paths.SCENARIOS_DIR / "industries").glob("*/*/intake.json")
    )

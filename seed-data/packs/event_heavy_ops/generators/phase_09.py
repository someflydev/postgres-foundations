"""Generate deterministic Phase 9 partition metadata under tmp/."""

from __future__ import annotations

import csv
from datetime import UTC, datetime
from pathlib import Path

MONTHS = (
    "2025-05",
    "2025-06",
    "2025-07",
    "2025-08",
    "2025-09",
    "2025-10",
    "2025-11",
    "2025-12",
    "2026-01",
    "2026-02",
    "2026-03",
    "2026-04",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def main() -> None:
    output_dir = repo_root() / "tmp" / "generated-seed-data" / "event_heavy_ops" / "phase-09"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "partition_manifest.csv"
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["partition_name", "from_bound", "to_bound", "planned_state"])
        for idx, month in enumerate(MONTHS):
            year, month_number = (int(part) for part in month.split("-"))
            from_bound = datetime(year, month_number, 1, tzinfo=UTC)
            if month_number == 12:
                to_bound = datetime(year + 1, 1, 1, tzinfo=UTC)
            else:
                to_bound = datetime(year, month_number + 1, 1, tzinfo=UTC)
            state = "detached-cold" if idx == 0 else "attached-hot"
            writer.writerow(
                [
                    f"event_log_partitioned_{year}_{month_number:02d}",
                    from_bound.isoformat(),
                    to_bound.isoformat(),
                    state,
                ]
            )
    print(path)


if __name__ == "__main__":
    main()

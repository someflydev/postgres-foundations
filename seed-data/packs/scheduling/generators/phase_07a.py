"""Generate deterministic phase 7a scheduling CSV fixtures under tmp/."""

from __future__ import annotations

import csv
from datetime import UTC, datetime, timedelta
from pathlib import Path

CLIENT_COUNT = 8_000
APPOINTMENT_COUNT = 50_000


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def write_csv(path: Path, header: tuple[str, ...], rows: list[tuple[object, ...]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(rows)


def main() -> None:
    output_dir = repo_root() / "tmp" / "generated-seed-data" / "scheduling" / "phase-07a"
    base_time = datetime(2025, 9, 1, 13, 0, tzinfo=UTC)

    clients = [
        (
            f"phase7a-client-{idx:05d}@example.com",
            f"Phase 7A Client {idx:05d}",
            (base_time - timedelta(days=idx % 120)).isoformat(),
        )
        for idx in range(1, CLIENT_COUNT + 1)
    ]
    write_csv(output_dir / "clients.csv", ("email", "full_name", "created_at"), clients)

    professionals = [
        "Dr. Rivera",
        "Dr. Chen",
        "Dr. Malik",
        "Dr. Alvarez",
        "Dr. Brooks",
        "Dr. Coleman",
        "Dr. Diaz",
        "Dr. Evans",
        "Dr. Foster",
        "Dr. Gupta",
    ]
    statuses = ("scheduled", "completed", "cancelled")
    appointments: list[tuple[object, ...]] = []
    for idx in range(1, APPOINTMENT_COUNT + 1):
        pro_name = professionals[(idx - 1) % len(professionals)]
        day_offset = (idx - 1) // len(professionals)
        starts_at = base_time + timedelta(days=day_offset, hours=(idx % 8))
        appointments.append(
            (
                pro_name,
                f"phase7a-client-{(((idx * 29) % CLIENT_COUNT) + 1):05d}@example.com",
                starts_at.isoformat(),
                (starts_at + timedelta(minutes=45)).isoformat(),
                statuses[idx % len(statuses)],
            )
        )

    write_csv(
        output_dir / "appointments.csv",
        ("professional_name", "client_email", "starts_at", "ends_at", "status"),
        appointments,
    )
    print(output_dir)


if __name__ == "__main__":
    main()

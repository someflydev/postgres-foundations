import json
from pathlib import Path

from pgfound.content import seed_doctor


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def test_seed_doctor_reports_missing_phase_sql(tmp_path: Path) -> None:
    exercises_dir = tmp_path / "exercises"
    seed_packs_dir = tmp_path / "seed-data" / "packs"
    exercise_dir = exercises_dir / "phase-01" / "lesson" / "level-a" / "missing-phase"
    _write_json(
        exercise_dir / "exercise.json",
        {
            "id": "missing-phase",
            "schema_scope": {"phase": "2"},
            "dataset": {"seed_pack_id": "ecommerce"},
            "solution_path": "solution.sql",
        },
    )
    (exercise_dir / "solution.sql").write_text(
        "SELECT id FROM ecommerce.customers;\n",
        encoding="utf-8",
    )
    phase_dir = seed_packs_dir / "ecommerce" / "phases"
    phase_dir.mkdir(parents=True)
    (phase_dir / "phase-01.sql").write_text(
        "CREATE SCHEMA IF NOT EXISTS ecommerce;\nCREATE TABLE ecommerce.customers (id bigint);\n",
        encoding="utf-8",
    )

    report = seed_doctor.run_seed_doctor(
        exercises_dir=exercises_dir,
        seed_packs_dir=seed_packs_dir,
    )

    assert not report.ok
    assert report.exercises_checked == 1
    assert "missing referenced phase SQL" in report.issues[0].message


def test_seed_doctor_reports_solution_table_missing_from_seed(tmp_path: Path) -> None:
    exercises_dir = tmp_path / "exercises"
    seed_packs_dir = tmp_path / "seed-data" / "packs"
    exercise_dir = exercises_dir / "phase-01" / "lesson" / "level-a" / "missing-table"
    _write_json(
        exercise_dir / "exercise.json",
        {
            "id": "missing-table",
            "schema_scope": {"phase": "1"},
            "dataset": {"seed_pack_id": "ecommerce"},
            "solution_path": "solution.sql",
        },
    )
    (exercise_dir / "solution.sql").write_text(
        "SELECT id FROM ecommerce.orders;\n",
        encoding="utf-8",
    )
    phase_dir = seed_packs_dir / "ecommerce" / "phases"
    phase_dir.mkdir(parents=True)
    (phase_dir / "phase-01.sql").write_text(
        "CREATE SCHEMA IF NOT EXISTS ecommerce;\nCREATE TABLE ecommerce.customers (id bigint);\n",
        encoding="utf-8",
    )

    report = seed_doctor.run_seed_doctor(
        exercises_dir=exercises_dir,
        seed_packs_dir=seed_packs_dir,
    )

    assert not report.ok
    assert "ecommerce.orders" in report.issues[0].message

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


def test_seed_doctor_accepts_lettered_phase_for_numeric_scope(tmp_path: Path) -> None:
    exercises_dir = tmp_path / "exercises"
    seed_packs_dir = tmp_path / "seed-data" / "packs"
    exercise_dir = exercises_dir / "phase-04" / "lesson" / "level-a" / "lettered-phase"
    _write_json(
        exercise_dir / "exercise.json",
        {
            "id": "lettered-phase",
            "schema_scope": {"phase": "4"},
            "dataset": {"seed_pack_id": "ecommerce"},
            "solution_path": "solution.sql",
        },
    )
    (exercise_dir / "solution.sql").write_text(
        "SELECT id FROM ecommerce.products;\n",
        encoding="utf-8",
    )
    phase_dir = seed_packs_dir / "ecommerce" / "phases"
    phase_dir.mkdir(parents=True)
    (phase_dir / "phase-04a.sql").write_text(
        "CREATE TABLE ecommerce.products (id bigint);\n",
        encoding="utf-8",
    )

    report = seed_doctor.run_seed_doctor(
        exercises_dir=exercises_dir,
        seed_packs_dir=seed_packs_dir,
    )

    assert report.ok


def test_seed_doctor_accepts_root_level_admin_sql_pack(tmp_path: Path) -> None:
    exercises_dir = tmp_path / "exercises"
    seed_packs_dir = tmp_path / "seed-data" / "packs"
    exercise_dir = exercises_dir / "admin" / "a1" / "lesson" / "level-a" / "admin-root-pack"
    _write_json(
        exercise_dir / "exercise.json",
        {
            "id": "admin-root-pack",
            "schema_scope": {"phase": "10"},
            "dataset": {"seed_pack_id": "admin"},
            "solution_path": "solution.sql",
        },
    )
    (exercise_dir / "solution.sql").write_text(
        "SELECT role_name FROM admin.role_matrix;\n",
        encoding="utf-8",
    )
    pack_dir = seed_packs_dir / "admin"
    pack_dir.mkdir(parents=True)
    (pack_dir / "roles-matrix.sql").write_text(
        "CREATE TABLE admin.role_matrix (role_name text);\n",
        encoding="utf-8",
    )

    report = seed_doctor.run_seed_doctor(
        exercises_dir=exercises_dir,
        seed_packs_dir=seed_packs_dir,
    )

    assert report.ok


def test_seed_doctor_ignores_comment_and_grant_targets(tmp_path: Path) -> None:
    exercises_dir = tmp_path / "exercises"
    seed_packs_dir = tmp_path / "seed-data" / "packs"
    exercise_dir = exercises_dir / "admin" / "a1" / "lesson" / "level-c" / "grant-only"
    _write_json(
        exercise_dir / "exercise.json",
        {
            "id": "grant-only",
            "schema_scope": {"phase": "10"},
            "dataset": {"seed_pack_id": "saas_multi_tenant"},
            "solution_path": "solution.sql",
        },
    )
    (exercise_dir / "solution.sql").write_text(
        "-- Review evidence should be captured from access-review-queries.sql.\n"
        "REVOKE ALL ON SCHEMA saas FROM app_api_login;\n"
        "GRANT saas_app_readwrite TO app_api_login;\n",
        encoding="utf-8",
    )
    phase_dir = seed_packs_dir / "saas_multi_tenant" / "phases"
    phase_dir.mkdir(parents=True)
    (phase_dir / "phase-10.sql").write_text(
        "CREATE SCHEMA saas;\n",
        encoding="utf-8",
    )

    report = seed_doctor.run_seed_doctor(
        exercises_dir=exercises_dir,
        seed_packs_dir=seed_packs_dir,
    )

    assert report.ok


def test_seed_doctor_accepts_declared_schema_scope_tables(tmp_path: Path) -> None:
    exercises_dir = tmp_path / "exercises"
    seed_packs_dir = tmp_path / "seed-data" / "packs"
    exercise_dir = exercises_dir / "extensions" / "postgis" / "lesson" / "level-a" / "declared"
    _write_json(
        exercise_dir / "exercise.json",
        {
            "id": "declared",
            "schema_scope": {"phase": "4", "tables": ["logistics.delivery_zones"]},
            "dataset": {"seed_pack_id": "logistics_geo"},
            "solution_path": "solution.sql",
        },
    )
    (exercise_dir / "solution.sql").write_text(
        "SELECT id FROM logistics.delivery_zones;\n",
        encoding="utf-8",
    )
    phase_dir = seed_packs_dir / "logistics_geo" / "phases"
    phase_dir.mkdir(parents=True)
    (phase_dir / "phase-01.sql").write_text(
        "CREATE SCHEMA logistics;\n",
        encoding="utf-8",
    )

    report = seed_doctor.run_seed_doctor(
        exercises_dir=exercises_dir,
        seed_packs_dir=seed_packs_dir,
    )

    assert report.ok

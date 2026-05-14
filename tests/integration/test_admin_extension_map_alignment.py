from __future__ import annotations

import json

from pgfound import paths


def test_admin_modules_have_populated_lesson_directories() -> None:
    data = json.loads((paths.CURRICULUM_DIR / "admin" / "map.json").read_text(encoding="utf-8"))
    module_ids = [module["id"] for module in data["modules"]]
    assert [module_id[:2] for module_id in module_ids] == ["a1", "a2", "a3", "a4", "a5", "a6"]

    for module in data["modules"]:
        lesson_dir = paths.LESSONS_DIR / "admin" / module["id"]
        assert lesson_dir.is_dir(), module["id"]
        assert list(lesson_dir.glob("*/lesson.json")), module["id"]


def test_extension_modules_have_lessons_exercises_and_catalog_alignment() -> None:
    data = json.loads(
        (paths.CURRICULUM_DIR / "extensions" / "map.json").read_text(encoding="utf-8")
    )
    modules = data["modules"]

    for module in modules:
        assert not module.get("deferred", False), module["id"]
        lesson_dir = paths.LESSONS_DIR / "extensions" / module["id"]
        exercise_dir = paths.EXERCISES_DIR / "extensions" / module["id"]
        assert list(lesson_dir.glob("*/lesson.json")), module["id"]
        assert list(exercise_dir.glob("*/*/*/exercise.json")), module["id"]

    module_ids = {module["id"] for module in modules}
    lesson_ids = {
        json.loads(path.read_text(encoding="utf-8"))["id"]
        for path in paths.LESSONS_DIR.rglob("lesson.json")
    }
    catalog = json.loads(
        (paths.DECISION_ENGINE_DIR / "catalogs" / "extensions.json").read_text(encoding="utf-8")
    )
    for extension in catalog:
        assert extension["module_slug"] in module_ids | lesson_ids, extension["id"]


def test_admin_modules_have_decision_engine_training_references() -> None:
    admin = json.loads((paths.CURRICULUM_DIR / "admin" / "map.json").read_text(encoding="utf-8"))
    admin_module_ids = {module["id"] for module in admin["modules"]}
    referenced: set[str] = set()

    for catalog_path in (paths.DECISION_ENGINE_DIR / "catalogs").glob("*.json"):
        entries = json.loads(catalog_path.read_text(encoding="utf-8"))
        for entry in entries:
            referenced.update(entry.get("training_modules", []))

    assert admin_module_ids <= referenced

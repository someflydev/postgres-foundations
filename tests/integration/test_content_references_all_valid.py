from __future__ import annotations

import json
import re
from pathlib import Path

from pgfound import paths

MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)#][^)]*)\)")


def _json_files(root: Path, name: str) -> list[Path]:
    return sorted(root.rglob(name))


def _load_all(root: Path, name: str) -> dict[str, tuple[Path, dict]]:
    records = {}
    for path in _json_files(root, name):
        data = json.loads(path.read_text(encoding="utf-8"))
        records[data["id"]] = (path, data)
    return records


def test_content_cross_references_resolve() -> None:
    lessons = _load_all(paths.LESSONS_DIR, "lesson.json")
    exercises = _load_all(paths.EXERCISES_DIR, "exercise.json")
    capstones = _load_all(paths.CAPSTONES_DIR, "capstone.json")
    scenarios = _load_all(paths.SCENARIOS_DIR, "scenario.json")
    rubrics = _load_all(paths.RUBRICS_DIR, "*.rubric.json")
    docs = set()
    for path in paths.REPO_ROOT.glob("docs/**/*.md"):
        relative_stem = path.relative_to(paths.REPO_ROOT / "docs").with_suffix("")
        docs.add(path.stem)
        docs.add(path.stem.replace("_", "-"))
        docs.add("-".join(relative_stem.parts).replace("_", "-"))
    docs.update(path.parent.name for path in paths.REPO_ROOT.glob("docs/**/README.md"))
    docs.add("postgres_docs_select")
    adr = {path.stem for path in (paths.REPO_ROOT / "docs" / "adr").glob("*.md")}

    indexes = {
        "lesson": lessons,
        "exercise": exercises,
        "scenario": scenarios,
        "capstone": capstones,
        "rubric": rubrics,
        "doc": {slug: (Path(), {}) for slug in docs},
        "adr": {slug: (Path(), {}) for slug in adr},
    }
    errors = []

    for lesson_id, (path, lesson) in lessons.items():
        for key in ("body_path", "worked_example_path"):
            if key in lesson and not (path.parent / lesson[key]).is_file():
                errors.append(f"{path}: {key} does not resolve")
        for ref in lesson.get("references", []):
            if ref["kind"] != "external" and ref["slug"] not in indexes[ref["kind"]]:
                errors.append(f"{path}: reference {ref['kind']}:{ref['slug']} does not resolve")

    for exercise_id, (path, exercise) in exercises.items():
        if exercise["lesson_id"] not in lessons:
            errors.append(f"{path}: lesson_id {exercise['lesson_id']} does not resolve")
        for key in ("solution_path", "starter_path"):
            if key in exercise and not (path.parent / exercise[key]).is_file():
                errors.append(f"{path}: {key} does not resolve")

    for capstone_id, (path, capstone) in capstones.items():
        for deliverable in capstone["deliverables"]:
            deliverable_path = Path(deliverable["path"])
            if (
                not (path.parent / deliverable_path).is_file()
                and not (paths.REPO_ROOT / deliverable_path).is_file()
            ):
                errors.append(f"{path}: deliverable {deliverable['path']} does not resolve")
        if (
            "critical_queries_path" in capstone
            and not (path.parent / capstone["critical_queries_path"]).is_file()
            and not (path.parent / "reference" / capstone["critical_queries_path"]).is_file()
            and not (paths.REPO_ROOT / capstone["critical_queries_path"]).is_file()
        ):
            errors.append(f"{path}: critical_queries_path does not resolve")

    for scenario_id, (path, scenario) in scenarios.items():
        for lesson_id in scenario.get("suggested_lessons", []):
            if lesson_id not in lessons:
                errors.append(f"{path}: suggested lesson {lesson_id} does not resolve")
        for exercise_id in scenario.get("suggested_exercises", []):
            if exercise_id not in exercises:
                errors.append(f"{path}: suggested exercise {exercise_id} does not resolve")
        capstone_id = scenario.get("suggested_capstone_id")
        if capstone_id and capstone_id not in capstones:
            errors.append(f"{path}: suggested capstone {capstone_id} does not resolve")

    anti_patterns = json.loads(
        (paths.DECISION_ENGINE_DIR / "catalogs" / "anti_patterns.json").read_text(encoding="utf-8")
    )
    for entry in anti_patterns:
        references = entry.get("references", [])
        if references:
            for reference in references:
                if not (paths.REPO_ROOT / reference).is_file():
                    errors.append(f"anti-pattern doc does not resolve: {reference}")
        else:
            doc_slug = entry.get("doc_slug", entry["id"])
            if not (paths.REPO_ROOT / "docs" / "anti-patterns" / f"{doc_slug}.md").is_file():
                errors.append(f"anti-pattern doc does not resolve: {doc_slug}")

    assert not errors


def test_docs_relative_markdown_links_resolve() -> None:
    errors = []
    for path in sorted((paths.REPO_ROOT / "docs").rglob("*.md")):
        for link in MD_LINK_RE.findall(path.read_text(encoding="utf-8")):
            target = link.split()[0]
            if "://" in target or target.startswith("mailto:"):
                continue
            if target.startswith("/docs/"):
                resolved = paths.REPO_ROOT / target.lstrip("/")
            elif target.startswith(("./", "../")):
                resolved = (path.parent / target).resolve()
            else:
                continue
            if not resolved.exists():
                errors.append(f"{path.relative_to(paths.REPO_ROOT)}: {target}")
    assert not errors

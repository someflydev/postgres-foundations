from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from pgfound import paths
from pgfound.content import lint, validate

E3 = "e3-postgis"
E4 = "e4-pgvector"
E3_LESSONS = {
    "geometry-vs-geography",
    "srid-and-transforms",
    "common-predicates",
    "spatial-indexing-with-gist",
    "service-zone-queries",
    "routing-preview",
    "raster-preview",
    "postgis-operational-cost",
    "anti-pattern-geo-logic-without-postgis",
    "when-postgis-is-right-and-wrong",
}
E4_LESSONS = {
    "what-vectors-are-for",
    "storage-and-dimensionality",
    "distance-metrics",
    "exact-vs-approximate-search",
    "hnsw-vs-ivfflat",
    "hybrid-retrieval-with-fts-and-trigrams",
    "metadata-filters-plus-embeddings",
    "cost-and-caveats",
    "when-vectors-are-the-right-answer",
}
WORD_RE = re.compile(r"\b[\w'-]+\b")


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_extension_e3_e4_validate_and_lint_cleanly() -> None:
    report = validate.validate_content(
        path_globs=(
            "curriculum/extensions/map.json",
            "lessons/extensions/**/*.json",
            "exercises/extensions/**/*.json",
            "rubrics/default/*.rubric.json",
        )
    )
    assert report.ok, [f"{issue.path}: {issue.message}" for issue in report.errors]

    lint_report = lint.lint_content(
        path_globs=("lessons/extensions/**/*.json", "exercises/extensions/**/*.json")
    )
    assert lint_report.ok, [f"{issue.path}: {issue.message}" for issue in lint_report.warnings]


def test_extension_e3_e4_lessons_and_distribution() -> None:
    e3_paths = sorted((paths.LESSONS_DIR / "extensions" / E3).glob("*/lesson.json"))
    e4_paths = sorted((paths.LESSONS_DIR / "extensions" / E4).glob("*/lesson.json"))
    assert {path.parent.name for path in e3_paths} == E3_LESSONS
    assert {path.parent.name for path in e4_paths} == E4_LESSONS

    exercises_by_lesson: dict[str, list[dict]] = defaultdict(list)
    for exercise_path in (paths.EXERCISES_DIR / "extensions").glob("*/*/*/*/exercise.json"):
        exercise = _load(exercise_path)
        exercises_by_lesson[exercise["lesson_id"]].append(exercise)

    lesson_ids = [_load(path)["id"] for path in e3_paths + e4_paths]
    assert sum(len(exercises_by_lesson[lesson_id]) for lesson_id in lesson_ids) == 152

    for lesson_path in e3_paths + e4_paths:
        lesson = _load(lesson_path)
        assert lesson["module_id"] == lesson_path.parent.parent.name
        body = (lesson_path.parent / lesson["body_path"]).read_text(encoding="utf-8")
        assert len(WORD_RE.findall(body)) >= 400
        levels = [exercise["scaffolding_level"] for exercise in exercises_by_lesson[lesson["id"]]]
        assert levels.count("A") == 2
        assert levels.count("B") == 2
        assert levels.count("C") == 2
        assert levels.count("D") == 2


def test_extension_e3_e4_critical_drills_docs_and_seeds_are_present() -> None:
    exercise_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (paths.EXERCISES_DIR / "extensions").glob("**/*")
        if path.is_file() and path.suffix in {".json", ".md", ".sql"}
    )
    assert "hourly counts per service zone using ST_Contains with a GiST index" in exercise_text
    assert "DIY Haversine in SQL" in exercise_text
    assert "HNSW-based vector retrieval over the document_search domain" in exercise_text
    assert (
        "predicate filter is applied after approximate search and dropping recall" in exercise_text
    )
    assert "pg_trgm would have solved the lexical problem" in exercise_text

    assert (paths.REPO_ROOT / "docs/extension-track/e3-postgis.md").is_file()
    assert (paths.REPO_ROOT / "docs/extension-track/e4-pgvector.md").is_file()
    assert (paths.REPO_ROOT / "docs/anti-patterns/geo_logic_without_postgis.md").is_file()
    assert (paths.REPO_ROOT / "docs/anti-patterns/vector_before_lexical.md").is_file()

    search_playbook = (paths.REPO_ROOT / "docs/search-playbook.md").read_text(encoding="utf-8")
    assert "docs/extension-track/e4-pgvector.md" in search_playbook

    geo_seed = paths.REPO_ROOT / "seed-data/packs/logistics_geo/geojson/service_zones.geojson"
    assert geo_seed.is_file()
    assert "ST_GeomFromGeoJSON" in (
        paths.REPO_ROOT / "seed-data/packs/logistics_geo/phases/phase-01.sql"
    ).read_text(encoding="utf-8")

    doc_seed = (paths.REPO_ROOT / "seed-data/packs/document_search/phases/phase-08.sql").read_text(
        encoding="utf-8"
    )
    assert "fake_embedding vector(16)" in doc_seed
    assert "docs_fake_embedding_hnsw_idx" in doc_seed

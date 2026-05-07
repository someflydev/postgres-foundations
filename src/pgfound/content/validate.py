"""Content schema validation and cross-file checks."""

from __future__ import annotations

import glob
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

import yaml
from jsonschema import Draft202012Validator, RefResolver
from jsonschema.exceptions import ValidationError

from pgfound import paths

CONTENT_KINDS: Final[tuple[str, ...]] = (
    "curriculum",
    "lesson",
    "exercise",
    "rubric",
    "scenario",
    "capstone",
)
SCHEMA_FILENAMES: Final[dict[str, str]] = {
    "curriculum": "curriculum.schema.json",
    "lesson": "lesson.schema.json",
    "exercise": "exercise.schema.json",
    "rubric": "rubric.schema.json",
    "scenario": "scenario.schema.json",
    "capstone": "capstone.schema.json",
}
CONTENT_DIR_NAMES: Final[dict[str, str]] = {
    "lesson": "lessons",
    "exercise": "exercises",
    "rubric": "rubrics",
    "scenario": "scenarios",
    "capstone": "capstones",
}
ROOT_CONTENT_FILES: Final[dict[str, Path]] = {
    "curriculum": paths.CURRICULUM_DIR / "map.json",
}
CONTENT_SUFFIXES: Final[set[str]] = {".json", ".yaml", ".yml"}
EXAMPLE_SUFFIX: Final[str] = ".example"


@dataclass(frozen=True)
class ValidationIssue:
    kind: str
    path: Path
    message: str
    severity: str = "error"


@dataclass(frozen=True)
class LoadedContent:
    kind: str
    path: Path
    data: dict[str, Any]


@dataclass(frozen=True)
class ValidationReport:
    files_checked: int
    errors: tuple[ValidationIssue, ...]
    warnings: tuple[ValidationIssue, ...]
    by_kind: dict[str, int]

    @property
    def ok(self) -> bool:
        return not self.errors


def schema_dir() -> Path:
    return paths.REPO_ROOT / "content-schemas"


def load_schema(kind: str) -> dict[str, Any]:
    return json.loads((schema_dir() / SCHEMA_FILENAMES[kind]).read_text(encoding="utf-8"))


def schema_store() -> dict[str, dict[str, Any]]:
    store = {}
    for schema_path in schema_dir().glob("*.json"):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        if "$id" in schema:
            store[schema["$id"]] = schema
        store[schema_path.name] = schema
    return store


def validator_for(kind: str) -> Draft202012Validator:
    schema = load_schema(kind)
    resolver = RefResolver(
        base_uri=f"{schema_dir().resolve().as_uri()}/",
        referrer=schema,
        store=schema_store(),
    )
    return Draft202012Validator(schema, resolver=resolver)


def validate_schema_files() -> None:
    for schema_path in sorted(schema_dir().glob("*.json")):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def discover_content_files(
    *,
    path_globs: tuple[str, ...] = (),
    include_examples: bool = False,
) -> list[Path]:
    if path_globs:
        files: set[Path] = set()
        for path_glob in path_globs:
            pattern = (
                path_glob if Path(path_glob).is_absolute() else str(paths.REPO_ROOT / path_glob)
            )
            for matched in glob.glob(pattern, recursive=True):
                matched_path = Path(matched)
                if matched_path.is_file() and matched_path.suffix.lower() in CONTENT_SUFFIXES:
                    files.add(matched_path.resolve())
        return sorted(files)

    files = []
    files.extend(path for path in ROOT_CONTENT_FILES.values() if path.exists())
    for directory_name in CONTENT_DIR_NAMES.values():
        directory = paths.CURRICULUM_DIR / directory_name
        if not directory.exists():
            continue
        files.extend(
            path
            for path in directory.rglob("*")
            if path.is_file() and path.suffix.lower() in CONTENT_SUFFIXES
        )

    if include_examples:
        examples_dir = schema_dir() / "examples"
        files.extend(
            path
            for path in examples_dir.glob("*.json")
            if path.is_file() and path.suffix.lower() in CONTENT_SUFFIXES
        )

    return sorted(files)


def infer_kind(file_path: Path) -> str | None:
    parts = set(file_path.parts)
    if file_path.name == "map.json" and file_path.parent.name == "curriculum":
        return "curriculum"
    for kind, directory_name in CONTENT_DIR_NAMES.items():
        if directory_name in parts:
            return kind

    stem = file_path.stem
    if stem.endswith(EXAMPLE_SUFFIX):
        stem = stem.removesuffix(EXAMPLE_SUFFIX)
    if stem in CONTENT_KINDS:
        return stem
    return None


def load_content_file(file_path: Path) -> dict[str, Any]:
    raw = file_path.read_text(encoding="utf-8")
    if file_path.suffix.lower() == ".json":
        loaded = json.loads(raw)
    else:
        loaded = yaml.safe_load(raw)
    if not isinstance(loaded, dict):
        msg = "content file must contain a JSON/YAML object"
        raise ValueError(msg)
    return loaded


def format_validation_error(error: ValidationError) -> str:
    location = ".".join(str(part) for part in error.absolute_path)
    prefix = f"{location}: " if location else ""
    return f"{prefix}{error.message}"


def validate_content(
    *,
    path_globs: tuple[str, ...] = (),
    include_examples: bool = False,
    strict: bool = False,
) -> ValidationReport:
    validate_schema_files()
    files = discover_content_files(path_globs=path_globs, include_examples=include_examples)
    validators = {kind: validator_for(kind) for kind in CONTENT_KINDS}
    loaded: list[LoadedContent] = []
    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []
    by_kind = {kind: 0 for kind in CONTENT_KINDS}

    for file_path in files:
        kind = infer_kind(file_path)
        if kind is None:
            warnings.append(
                ValidationIssue("unknown", file_path, "could not infer content kind", "warning")
            )
            continue
        by_kind[kind] += 1
        try:
            data = load_content_file(file_path)
        except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
            errors.append(ValidationIssue(kind, file_path, f"could not load file: {exc}"))
            continue

        validator = validators[kind]
        schema_errors = sorted(validator.iter_errors(data), key=lambda item: item.path)
        if schema_errors:
            errors.extend(
                ValidationIssue(kind, file_path, format_validation_error(error))
                for error in schema_errors
            )
        loaded.append(LoadedContent(kind=kind, path=file_path, data=data))

    errors.extend(_cross_file_errors(loaded))
    warnings.extend(_catalog_warnings(loaded))

    if strict and warnings:
        errors.extend(
            ValidationIssue(issue.kind, issue.path, issue.message, "error") for issue in warnings
        )
        warnings = []

    return ValidationReport(
        files_checked=len(files),
        errors=tuple(errors),
        warnings=tuple(warnings),
        by_kind=by_kind,
    )


def _content_by_id(loaded: list[LoadedContent], kind: str) -> dict[str, LoadedContent]:
    return {
        str(item.data["id"]): item
        for item in loaded
        if item.kind == kind and isinstance(item.data.get("id"), str)
    }


def _cross_file_errors(loaded: list[LoadedContent]) -> list[ValidationIssue]:
    errors: list[ValidationIssue] = []
    lessons = _content_by_id(loaded, "lesson")
    rubrics = _content_by_id(loaded, "rubric")

    for item in loaded:
        data = item.data
        if item.kind == "curriculum":
            errors.extend(_curriculum_errors(item))
        elif item.kind == "lesson":
            has_phase = "phase" in data
            has_module = "module_id" in data
            if has_phase == has_module:
                errors.append(
                    ValidationIssue(
                        item.kind,
                        item.path,
                        "lesson must carry exactly one of phase or module_id",
                    )
                )
        elif item.kind == "exercise":
            lesson_id = data.get("lesson_id")
            parent = lessons.get(str(lesson_id))
            if parent is None:
                errors.append(
                    ValidationIssue(item.kind, item.path, f"lesson_id {lesson_id!r} does not exist")
                )
            else:
                parent_boundary = set(parent.data.get("concepts_not_yet_allowed", []))
                exercise_boundary = set(data.get("not_yet_allowed_concepts", []))
                missing = sorted(parent_boundary - exercise_boundary)
                if missing:
                    errors.append(
                        ValidationIssue(
                            item.kind,
                            item.path,
                            "not_yet_allowed_concepts must include parent lesson boundary: "
                            + ", ".join(missing),
                        )
                    )
            rubric_id = data.get("rubric_id")
            if rubric_id and str(rubric_id) not in rubrics:
                errors.append(
                    ValidationIssue(item.kind, item.path, f"rubric_id {rubric_id!r} does not exist")
                )
        elif item.kind == "rubric":
            dimensions = data.get("dimensions", [])
            if isinstance(dimensions, list):
                total = sum(
                    dimension.get("weight", 0)
                    for dimension in dimensions
                    if isinstance(dimension, dict)
                    and isinstance(dimension.get("weight"), int | float)
                )
                if abs(total - 1.0) > 1e-6:
                    errors.append(
                        ValidationIssue(
                            item.kind,
                            item.path,
                            f"rubric dimension weights must sum to 1.0; got {total:.6f}",
                        )
                    )
    return errors


def _curriculum_errors(item: LoadedContent) -> list[ValidationIssue]:
    data = item.data
    errors: list[ValidationIssue] = []

    phases = data.get("phases", [])
    if isinstance(phases, list):
        numbers = [phase.get("number") for phase in phases if isinstance(phase, dict)]
        if numbers != list(range(11)):
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    f"phase numbers must be monotonic 0..10; got {numbers}",
                )
            )
        slugs = [phase.get("slug") for phase in phases if isinstance(phase, dict)]
        duplicate_slugs = _duplicates(slugs)
        if duplicate_slugs:
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    "phase slugs must be unique: " + ", ".join(duplicate_slugs),
                )
            )

    domains = data.get("domains", [])
    if isinstance(domains, list):
        duplicate_domains = _duplicates(
            domain.get("slug") for domain in domains if isinstance(domain, dict)
        )
        if duplicate_domains:
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    "domain slugs must be unique: " + ", ".join(duplicate_domains),
                )
            )

    capstones = data.get("capstones", [])
    if isinstance(capstones, list):
        duplicate_capstones = _duplicates(
            capstone.get("id") for capstone in capstones if isinstance(capstone, dict)
        )
        if duplicate_capstones:
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    "capstone ids must be unique: " + ", ".join(duplicate_capstones),
                )
            )

    return errors


def _duplicates(values: Any) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if not isinstance(value, str | int):
            continue
        key = str(value)
        if key in seen:
            duplicates.add(key)
        seen.add(key)
    return sorted(duplicates)


def _catalog_warnings(loaded: list[LoadedContent]) -> list[ValidationIssue]:
    scenario_items = [item for item in loaded if item.kind == "scenario"]
    if not scenario_items:
        return []

    catalogs_dir = paths.DECISION_ENGINE_DIR / "catalogs"
    warnings: list[ValidationIssue] = []
    catalog_specs = {
        "data_shapes": catalogs_dir / "data_shapes.json",
        "workload_patterns": catalogs_dir / "workload_patterns.json",
    }
    for field, catalog_path in catalog_specs.items():
        if not catalog_path.exists():
            for item in scenario_items:
                warnings.append(
                    ValidationIssue(
                        item.kind,
                        item.path,
                        f"decision-engine catalog missing; skipped {field} reference check",
                        "warning",
                    )
                )
            continue

        known_slugs = _load_catalog_slugs(catalog_path)
        for item in scenario_items:
            for slug in item.data.get(field, []):
                if slug not in known_slugs:
                    warnings.append(
                        ValidationIssue(
                            item.kind,
                            item.path,
                            f"{field} slug {slug!r} is not present in {catalog_path}",
                            "warning",
                        )
                    )
    return warnings


def _load_catalog_slugs(catalog_path: Path) -> set[str]:
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    return _extract_slugs(data)


def _extract_slugs(value: Any) -> set[str]:
    if isinstance(value, dict):
        slugs: set[str] = set()
        for key, item in value.items():
            if isinstance(item, dict):
                slug = item.get("slug") or item.get("id")
                if isinstance(slug, str):
                    slugs.add(slug)
                elif isinstance(key, str):
                    slugs.add(key)
                slugs.update(_extract_slugs(item))
            elif isinstance(item, list):
                slugs.update(_extract_slugs(item))
        return slugs
    if isinstance(value, list):
        slugs = set()
        for item in value:
            if isinstance(item, dict):
                slug = item.get("slug") or item.get("id")
                if isinstance(slug, str):
                    slugs.add(slug)
                slugs.update(_extract_slugs(item))
        return slugs
    return set()

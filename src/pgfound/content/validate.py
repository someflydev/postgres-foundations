"""Content schema validation and cross-file checks."""

from __future__ import annotations

import glob
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

import yaml
from jsonschema import Draft202012Validator, RefResolver
from jsonschema.exceptions import ValidationError

from pgfound import paths
from pgfound.decision import engine as decision_engine

CONTENT_KINDS: Final[tuple[str, ...]] = (
    "curriculum",
    "admin_map",
    "extension_map",
    "lesson",
    "exercise",
    "rubric",
    "scenario",
    "capstone",
)
SCHEMA_FILENAMES: Final[dict[str, str]] = {
    "curriculum": "curriculum.schema.json",
    "admin_map": "admin-map.schema.json",
    "extension_map": "extension-map.schema.json",
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
CONTENT_DIRS: Final[dict[str, Path]] = {
    "lesson": paths.LESSONS_DIR,
    "exercise": paths.EXERCISES_DIR,
    "rubric": paths.RUBRICS_DIR,
    "scenario": paths.SCENARIOS_DIR,
    "capstone": paths.CAPSTONES_DIR,
}
ROOT_CONTENT_FILES: Final[dict[str, Path]] = {
    "curriculum": paths.CURRICULUM_DIR / "map.json",
    "admin_map": paths.CURRICULUM_DIR / "admin" / "map.json",
    "extension_map": paths.CURRICULUM_DIR / "extensions" / "map.json",
}
CONTENT_SUFFIXES: Final[set[str]] = {".json", ".yaml", ".yml"}
EXAMPLE_SUFFIX: Final[str] = ".example"
PLACEHOLDER_RE: Final[re.Pattern[str]] = re.compile(
    r"__REPLACE_ME[^_]*__|__REPLACE_ME_[A-Z0-9_]+__"
)
PHASE_DIR_RE: Final[re.Pattern[str]] = re.compile(r"^phase-(?P<number>\d{2})-[a-z0-9-]+$")
EXERCISE_LEVEL_DIR_RE: Final[re.Pattern[str]] = re.compile(r"^level-(?P<level>[a-d])$")
PHASE_EXERCISE_OVERRIDES: Final[dict[int, dict[str, set[str]]]] = {
    0: {
        "solution_sql_optional_kinds": {"modeling"},
        "level_d_kinds": {"critique", "debug", "modeling"},
    },
    6: {
        "solution_sql_optional_kinds": {"critique", "debug", "lab"},
        "level_d_kinds": {"critique", "debug", "lab"},
    },
}


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
    return _validator_for_schema(schema)


def validator_for_schema_file(schema_filename: str) -> Draft202012Validator:
    schema = json.loads((schema_dir() / schema_filename).read_text(encoding="utf-8"))
    return _validator_for_schema(schema)


def _validator_for_schema(schema: dict[str, Any]) -> Draft202012Validator:
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
    for directory in CONTENT_DIRS.values():
        if not directory.exists():
            continue
        files.extend(
            path
            for path in directory.rglob("*")
            if path.is_file()
            and path.suffix.lower() in CONTENT_SUFFIXES
            and "concurrency" not in path.relative_to(directory).parts
            and not _is_industry_scenario_sidecar(path)
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
    if file_path.name == "rubric.json":
        return "rubric"
    if file_path.name == "capstone.json":
        return "capstone"
    parts = set(file_path.parts)
    if file_path.name == "map.json" and file_path.parent.name == "curriculum":
        return "curriculum"
    if (
        file_path.name == "map.json"
        and file_path.parent.name == "admin"
        and file_path.parent.parent.name == "curriculum"
    ):
        return "admin_map"
    if (
        file_path.name == "map.json"
        and file_path.parent.name == "extensions"
        and file_path.parent.parent.name == "curriculum"
    ):
        return "extension_map"
    for kind, directory_name in CONTENT_DIR_NAMES.items():
        if directory_name in parts:
            return kind

    stem = file_path.stem
    if stem.endswith(EXAMPLE_SUFFIX):
        stem = stem.removesuffix(EXAMPLE_SUFFIX)
    if stem in CONTENT_KINDS:
        return stem
    return None


def _is_interview_scenario_path(file_path: Path) -> bool:
    return "scenarios" in file_path.parts and "interviews" in file_path.parts


def _is_industry_scenario_sidecar(file_path: Path) -> bool:
    return (
        "scenarios" in file_path.parts
        and "industries" in file_path.parts
        and file_path.name in {"intake.json", "expected-report.json"}
    )


def _exercise_exists(exercise_id: str) -> bool:
    for exercise_path in paths.EXERCISES_DIR.rglob("exercise.json"):
        try:
            data = json.loads(exercise_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("id") == exercise_id:
            return True
    return False


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
    schema_only: bool = False,
) -> ValidationReport:
    validate_schema_files()
    files = discover_content_files(path_globs=path_globs, include_examples=include_examples)
    validators = {kind: validator_for(kind) for kind in CONTENT_KINDS}
    interview_scenario_validator = validator_for_schema_file("interview-scenario.schema.json")
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

        validator = (
            interview_scenario_validator
            if kind == "scenario" and _is_interview_scenario_path(file_path)
            else validators[kind]
        )
        schema_errors = sorted(validator.iter_errors(data), key=lambda item: item.path)
        if schema_errors:
            errors.extend(
                ValidationIssue(kind, file_path, format_validation_error(error))
                for error in schema_errors
            )
        loaded.append(LoadedContent(kind=kind, path=file_path, data=data))

    if not schema_only:
        cross_errors, cross_warnings = _cross_file_checks(loaded)
        errors.extend(cross_errors)
        warnings.extend(cross_warnings)
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


def _cross_file_checks(
    loaded: list[LoadedContent],
) -> tuple[list[ValidationIssue], list[ValidationIssue]]:
    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []
    lessons = _content_by_id(loaded, "lesson")
    rubrics = _content_by_id(loaded, "rubric")
    admin_module_ids = {
        str(module.get("id"))
        for item in loaded
        if item.kind == "admin_map"
        for module in item.data.get("modules", [])
        if isinstance(module, dict) and isinstance(module.get("id"), str)
    }
    extension_module_ids = {
        str(module.get("id"))
        for item in loaded
        if item.kind == "extension_map"
        for module in item.data.get("modules", [])
        if isinstance(module, dict) and isinstance(module.get("id"), str)
    }
    exercises_by_lesson: dict[str, list[LoadedContent]] = {}
    for exercise in (item for item in loaded if item.kind == "exercise"):
        lesson_id = exercise.data.get("lesson_id")
        if isinstance(lesson_id, str):
            exercises_by_lesson.setdefault(lesson_id, []).append(exercise)

    for item in loaded:
        data = item.data
        if item.kind == "curriculum":
            errors.extend(_curriculum_errors(item))
        elif item.kind == "admin_map":
            errors.extend(_admin_map_errors(item))
        elif item.kind == "extension_map":
            errors.extend(_extension_map_errors(item))
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
            errors.extend(
                _lesson_authoring_errors(
                    item,
                    admin_module_ids=admin_module_ids,
                    extension_module_ids=extension_module_ids,
                )
            )
            if data.get("status") == "active" and not exercises_by_lesson.get(str(data.get("id"))):
                warnings.append(
                    ValidationIssue(
                        item.kind,
                        item.path,
                        f"active lesson {data.get('id')!r} has no referencing exercises",
                        "warning",
                    )
                )
        elif item.kind == "exercise":
            errors.extend(
                _exercise_authoring_errors(
                    item,
                    parent=lessons.get(str(data.get("lesson_id"))),
                )
            )
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
            errors.extend(_rubric_composition_errors(item, rubrics))
        elif item.kind == "capstone":
            rubric_id = data.get("review_rubric_id")
            if rubric_id and str(rubric_id) not in rubrics:
                errors.append(
                    ValidationIssue(
                        item.kind,
                        item.path,
                        f"review_rubric_id {rubric_id!r} does not exist",
                    )
                )
        elif item.kind == "scenario" and _is_interview_scenario_path(item.path):
            errors.extend(_interview_scenario_errors(item, rubrics))
        elif item.kind == "scenario" and _is_industry_scenario_path(item.path):
            errors.extend(_industry_scenario_errors(item))
    return errors, warnings


def _is_industry_scenario_path(file_path: Path) -> bool:
    return (
        "scenarios" in file_path.parts
        and "industries" in file_path.parts
        and file_path.name == "scenario.json"
    )


def _masked_decision_report(report: dict[str, Any]) -> dict[str, Any]:
    masked = dict(report)
    masked["generated_at"] = "<generated_at>"
    masked["engine_version"] = decision_engine.ENGINE_VERSION
    return masked


def _industry_scenario_errors(item: LoadedContent) -> list[ValidationIssue]:
    errors: list[ValidationIssue] = []
    scenario_dir = item.path.parent
    intake_path = scenario_dir / "intake.json"
    expected_json_path = scenario_dir / "expected-report.json"
    expected_markdown_path = scenario_dir / "expected-report.md"
    narrative_path = scenario_dir / str(item.data.get("narrative_path", ""))

    for required_path in (intake_path, expected_json_path, expected_markdown_path, narrative_path):
        if not required_path.is_file():
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    f"required scenario artifact is missing: {required_path.name}",
                )
            )
    if errors:
        return errors

    try:
        report = decision_engine.run_decision(intake_path)
    except decision_engine.DecisionValidationError as exc:
        errors.append(ValidationIssue(item.kind, intake_path, str(exc)))
        return errors

    try:
        expected_report = json.loads(expected_json_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(
            ValidationIssue(
                item.kind,
                expected_json_path,
                f"could not load expected-report.json: {exc}",
            )
        )
        return errors

    try:
        decision_engine.validate_report(expected_report)
    except decision_engine.DecisionValidationError as exc:
        errors.append(ValidationIssue(item.kind, expected_json_path, str(exc)))
        return errors

    if _masked_decision_report(report) != _masked_decision_report(expected_report):
        errors.append(
            ValidationIssue(
                item.kind,
                expected_json_path,
                "expected-report.json is stale; run pgfound decision golden-refresh --dry-run",
            )
        )

    actual_by_class: dict[str, set[str]] = {
        "recommend_now": set(),
        "candidate_later": set(),
        "avoid_for_now": set(),
    }
    for recommendation in report["recommendations"]:
        recommendation_class = recommendation.get("recommendation_class")
        target_slug = recommendation.get("target_slug")
        if recommendation_class in actual_by_class and isinstance(target_slug, str):
            actual_by_class[recommendation_class].add(target_slug)

    expected_outputs = item.data.get("expected_decision_outputs", {})
    for recommendation_class, expected_slugs in expected_outputs.items():
        if recommendation_class not in actual_by_class or not isinstance(expected_slugs, list):
            continue
        missing = sorted(set(expected_slugs) - actual_by_class[recommendation_class])
        if missing:
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    f"expected {recommendation_class} outputs missing from actual report: "
                    + ", ".join(missing),
                )
            )
    return errors


def _interview_scenario_errors(
    item: LoadedContent,
    rubrics: dict[str, LoadedContent],
) -> list[ValidationIssue]:
    errors: list[ValidationIssue] = []
    data = item.data
    rubric_id = str(data.get("rubric_id", ""))
    rubric = rubrics.get(rubric_id)
    if rubric is None:
        errors.append(
            ValidationIssue(item.kind, item.path, f"rubric_id {rubric_id!r} does not exist")
        )
    elif rubric.data.get("applies_to") != "interview":
        errors.append(
            ValidationIssue(
                item.kind, item.path, f"rubric_id {rubric_id!r} is not an interview rubric"
            )
        )

    duration = data.get("duration_minutes")
    stages = data.get("stages", [])
    if isinstance(duration, int) and isinstance(stages, list):
        total = sum(
            stage.get("budget_minutes", 0)
            for stage in stages
            if isinstance(stage, dict) and isinstance(stage.get("budget_minutes"), int)
        )
        if total > duration:
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    f"stage budgets sum to {total}, exceeding duration_minutes {duration}",
                )
            )
    for stage in stages if isinstance(stages, list) else []:
        if not isinstance(stage, dict):
            continue
        exercise_id = stage.get("exercise_id")
        if isinstance(exercise_id, str) and not _exercise_exists(exercise_id):
            errors.append(
                ValidationIssue(item.kind, item.path, f"exercise_id {exercise_id!r} does not exist")
            )
        template = stage.get("prompt_template")
        if isinstance(template, str) and not (paths.LLM_PROMPTS_DIR / f"{template}.md").is_file():
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    f"prompt_template {template!r} does not resolve to an existing template",
                )
            )
    return errors


def _rubric_composition_errors(
    item: LoadedContent, rubrics: dict[str, LoadedContent]
) -> list[ValidationIssue]:
    errors: list[ValidationIssue] = []
    data = item.data
    total = 0.0
    dimensions = data.get("dimensions", [])
    if isinstance(dimensions, list):
        total += _dimension_weight_total(dimensions)
    own_dimensions = data.get("own_dimensions", [])
    if isinstance(own_dimensions, list):
        total += _dimension_weight_total(own_dimensions)
    extends = data.get("extends", [])
    if isinstance(extends, list):
        for entry in extends:
            if not isinstance(entry, dict):
                continue
            rubric_id = str(entry.get("rubric_id", ""))
            if rubric_id == data.get("id"):
                errors.append(ValidationIssue(item.kind, item.path, "rubric cannot extend itself"))
            elif rubric_id and rubric_id not in rubrics:
                errors.append(
                    ValidationIssue(
                        item.kind,
                        item.path,
                        f"extended rubric_id {rubric_id!r} does not exist",
                    )
                )
            weight = entry.get("weight", 0)
            if isinstance(weight, int | float):
                total += weight

    if abs(total - 1.0) > 1e-6:
        errors.append(
            ValidationIssue(
                item.kind,
                item.path,
                f"rubric dimension weights must sum to 1.0; got {total:.6f}",
            )
        )
    return errors


def _dimension_weight_total(dimensions: list[Any]) -> float:
    return sum(
        dimension.get("weight", 0)
        for dimension in dimensions
        if isinstance(dimension, dict) and isinstance(dimension.get("weight"), int | float)
    )


def _exercise_authoring_errors(
    item: LoadedContent,
    *,
    parent: LoadedContent | None,
) -> list[ValidationIssue]:
    errors: list[ValidationIssue] = []
    data = item.data
    if _is_schema_example(item.path):
        return errors

    allowed = set(data.get("allowed_concepts", []))
    not_yet_allowed = set(data.get("not_yet_allowed_concepts", []))
    overlap = sorted(allowed & not_yet_allowed)
    if overlap:
        errors.append(
            ValidationIssue(
                item.kind,
                item.path,
                "allowed_concepts overlaps not_yet_allowed_concepts: " + ", ".join(overlap),
            )
        )

    if item.path.name != "exercise.json":
        errors.append(
            ValidationIssue(
                item.kind,
                item.path,
                "authored exercise metadata must be exercise.json",
            )
        )
        return errors

    expected_level = data.get("scaffolding_level")
    level_dir = item.path.parent.parent.name
    level_match = EXERCISE_LEVEL_DIR_RE.match(level_dir)
    if not level_match:
        errors.append(
            ValidationIssue(
                item.kind,
                item.path,
                "exercise.json must be enclosed by a level-a, level-b, "
                "level-c, or level-d directory",
            )
        )
    elif isinstance(expected_level, str) and level_match.group("level").upper() != expected_level:
        errors.append(
            ValidationIssue(
                item.kind,
                item.path,
                f"scaffolding_level {expected_level!r} does not match enclosing {level_dir!r}",
            )
        )

    level = data.get("scaffolding_level")
    hints = data.get("hints", [])
    oral_defense = data.get("oral_defense_prompts", [])
    status = data.get("status")
    if level in {"C", "D"} and hints:
        errors.append(
            ValidationIssue(item.kind, item.path, "Level C and D exercises must not include hints")
        )
    if status == "active":
        if level == "C" and len(oral_defense) < 2:
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    "active Level C exercises require at least 2 oral_defense_prompts",
                )
            )
        if level == "D" and len(oral_defense) < 3:
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    "active Level D exercises require at least 3 oral_defense_prompts",
                )
            )
        if level in {"C", "D"} and any(
            isinstance(prompt, str) and PLACEHOLDER_RE.search(prompt) for prompt in oral_defense
        ):
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    "active oral_defense_prompts must not contain __REPLACE_ME__ placeholders",
                )
            )
        if (
            _requires_solution_sql(item, data, parent)
            and not (item.path.parent / "solution.sql").is_file()
        ):
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    "active executable exercises require solution.sql",
                )
            )

    if level == "D" and data.get("kind") not in _level_d_kinds(item, parent):
        errors.append(
            ValidationIssue(
                item.kind,
                item.path,
                "Level D exercises must use an allowed critique-and-repair kind",
            )
        )

    if parent is not None:
        lesson_slug = item.path.parent.parent.parent.name
        expected_lesson_dir = _lesson_dir_slug(parent.path)
        if expected_lesson_dir and lesson_slug != expected_lesson_dir:
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    "exercise path lesson slug "
                    f"{lesson_slug!r} does not match parent lesson directory "
                    f"{expected_lesson_dir!r}",
                )
            )

    prompt_path = item.path.parent / "prompt.md"
    solution_path = item.path.parent / data.get("solution_path", "")
    if not prompt_path.is_file():
        errors.append(ValidationIssue(item.kind, item.path, "prompt.md is missing"))
    if isinstance(data.get("solution_path"), str) and not solution_path.is_file():
        errors.append(
            ValidationIssue(
                item.kind,
                item.path,
                f"solution_path {data.get('solution_path')!r} does not resolve to an existing file",
            )
        )
    return errors


def _requires_solution_sql(
    item: LoadedContent,
    data: dict[str, Any],
    parent: LoadedContent | None,
) -> bool:
    kind = data.get("kind")
    phase = parent.data.get("phase") if parent is not None else _phase_from_path(item.path)
    if isinstance(phase, int):
        optional_kinds = PHASE_EXERCISE_OVERRIDES.get(phase, {}).get(
            "solution_sql_optional_kinds",
            set(),
        )
        if isinstance(kind, str) and kind in optional_kinds:
            return False
    return kind in {"query", "schema", "lab"}


def _level_d_kinds(item: LoadedContent, parent: LoadedContent | None) -> set[str]:
    phase = parent.data.get("phase") if parent is not None else _phase_from_path(item.path)
    if isinstance(phase, int):
        override = PHASE_EXERCISE_OVERRIDES.get(phase, {}).get("level_d_kinds")
        if override:
            return override
    return {"critique", "debug"}


def _phase_from_path(path: Path) -> int | None:
    for part in path.parts:
        match = PHASE_DIR_RE.match(part)
        if match:
            return int(match.group("number"))
    return None


def _lesson_dir_slug(path: Path) -> str | None:
    if path.name == "lesson.json":
        return path.parent.name
    return None


def _lesson_authoring_errors(
    item: LoadedContent,
    *,
    admin_module_ids: set[str] | None = None,
    extension_module_ids: set[str] | None = None,
) -> list[ValidationIssue]:
    errors: list[ValidationIssue] = []
    data = item.data
    if _is_schema_example(item.path):
        return errors

    introduced = set(data.get("concepts_introduced", []))
    not_yet_allowed = set(data.get("concepts_not_yet_allowed", []))
    overlap = sorted(introduced & not_yet_allowed)
    if overlap:
        errors.append(
            ValidationIssue(
                item.kind,
                item.path,
                "concepts_not_yet_allowed overlaps concepts_introduced: " + ", ".join(overlap),
            )
        )

    if data.get("status") == "active":
        raw_lesson = item.path.read_text(encoding="utf-8")
        if PLACEHOLDER_RE.search(raw_lesson):
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    "active lesson.json must not contain __REPLACE_ME__ placeholders",
                )
            )

    if item.path.name != "lesson.json":
        return errors

    body_path = data.get("body_path")
    if isinstance(body_path, str):
        resolved_body = item.path.parent / body_path
        if not resolved_body.is_file():
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    f"body_path {body_path!r} does not resolve to an existing file",
                )
            )
        elif data.get("status") == "active":
            raw_body = resolved_body.read_text(encoding="utf-8")
            if PLACEHOLDER_RE.search(raw_body):
                errors.append(
                    ValidationIssue(
                        item.kind,
                        resolved_body,
                        "active body.md must not contain __REPLACE_ME__ placeholders",
                    )
                )

    phase = data.get("phase")
    module_id = data.get("module_id")
    phase_dir = item.path.parent.parent.parent.name
    match = PHASE_DIR_RE.match(phase_dir)
    if isinstance(phase, int):
        if match is None:
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    "lesson.json must be enclosed by a phase-NN-slug directory",
                )
            )
        elif int(match.group("number")) != phase:
            errors.append(
                ValidationIssue(
                    item.kind,
                    item.path,
                    f"lesson.phase {phase} does not match enclosing directory {phase_dir!r}",
                )
            )
    elif isinstance(module_id, str):
        parts = item.path.parts
        if "lessons" in parts and "admin" in parts:
            module_dir = item.path.parent.parent.name
            if module_dir != module_id:
                errors.append(
                    ValidationIssue(
                        item.kind,
                        item.path,
                        f"lesson.module_id {module_id!r} does not match enclosing directory "
                        f"{module_dir!r}",
                    )
                )
            if (
                admin_module_ids is not None
                and admin_module_ids
                and module_id not in admin_module_ids
            ):
                errors.append(
                    ValidationIssue(
                        item.kind,
                        item.path,
                        f"lesson.module_id {module_id!r} is not present in "
                        "curriculum/admin/map.json",
                    )
                )
        elif "lessons" in parts and "extensions" in parts:
            module_dir = item.path.parent.parent.name
            if module_dir != module_id:
                errors.append(
                    ValidationIssue(
                        item.kind,
                        item.path,
                        f"lesson.module_id {module_id!r} does not match enclosing directory "
                        f"{module_dir!r}",
                    )
                )
            if (
                extension_module_ids is not None
                and extension_module_ids
                and module_id not in extension_module_ids
            ):
                errors.append(
                    ValidationIssue(
                        item.kind,
                        item.path,
                        f"lesson.module_id {module_id!r} is not present in "
                        "curriculum/extensions/map.json",
                    )
                )
    return errors


def _admin_map_errors(item: LoadedContent) -> list[ValidationIssue]:
    data = item.data
    errors: list[ValidationIssue] = []
    modules = data.get("modules", [])
    if not isinstance(modules, list):
        return errors

    ids = [module.get("id") for module in modules if isinstance(module, dict)]
    duplicate_ids = _duplicates(ids)
    if duplicate_ids:
        errors.append(
            ValidationIssue(
                item.kind,
                item.path,
                "admin module ids must be unique: " + ", ".join(duplicate_ids),
            )
        )

    expected = [
        "a1-roles-and-privileges",
        "a2-schemas-and-databases",
        "a3-auth-and-pooling",
        "a4-maintenance-and-lifecycle",
        "a5-monitoring-and-performance-ops",
        "a6-replication-and-ha",
    ]
    if ids != expected:
        errors.append(
            ValidationIssue(
                item.kind,
                item.path,
                f"admin module ids must be A1..A6 in order; got {ids}",
            )
        )
    return errors


def _extension_map_errors(item: LoadedContent) -> list[ValidationIssue]:
    data = item.data
    errors: list[ValidationIssue] = []
    modules = data.get("modules", [])
    if not isinstance(modules, list):
        return errors

    ids = [module.get("id") for module in modules if isinstance(module, dict)]
    duplicate_ids = _duplicates(ids)
    if duplicate_ids:
        errors.append(
            ValidationIssue(
                item.kind,
                item.path,
                "extension module ids must be unique: " + ", ".join(duplicate_ids),
            )
        )

    expected = [
        "e1-pg-stat-statements",
        "e2-pg-trgm",
        "e3-postgis",
        "e4-pgvector",
        "e5-timescaledb",
        "e6-postgres-fdw",
        "e7-citus",
        "ltree",
        "pg-partman",
        "pgbouncer",
    ]
    if ids != expected:
        errors.append(
            ValidationIssue(
                item.kind,
                item.path,
                f"extension module ids must be in canonical order; got {ids}",
            )
        )
    return errors


def _is_schema_example(path: Path) -> bool:
    try:
        path.relative_to(schema_dir() / "examples")
    except ValueError:
        return False
    return True


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
    scenario_items = [
        item
        for item in loaded
        if item.kind == "scenario" and not _is_interview_scenario_path(item.path)
    ]
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

"""Review engine orchestrator."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pgfound import exercise as exercise_runner
from pgfound import paths
from pgfound.llm import templates as llm_templates
from pgfound.review import grading
from pgfound.review.models import EvaluationRequest, EvaluationResult, Finding, Signal
from pgfound.review.output import json as json_output
from pgfound.review.output import report as report_output
from pgfound.review.runners import capstone as capstone_runner
from pgfound.review.runners import query, schema, writeup

DEFAULT_CAPSTONE_SECTIONS = [
    "Modeling",
    "Indexes",
    "RLS",
    "Operations",
    "Extension posture",
    "Not yet",
]


def evaluate(request: EvaluationRequest) -> EvaluationResult:
    """Evaluate an exercise or capstone request."""
    if request.target_kind == "exercise":
        return evaluate_exercise(request)
    if request.target_kind == "capstone":
        return evaluate_capstone(request)
    msg = f"unsupported review target kind: {request.target_kind}"
    raise ValueError(msg)


def evaluate_exercise(request: EvaluationRequest) -> EvaluationResult:
    """Run the exercise review flow."""
    record = exercise_runner.find_exercise(request.target_id)
    findings: list[Finding] = []
    signals: list[Signal] = []
    plan_diffs: list[dict[str, Any]] = []
    answer_path = request.artifact_path

    try:
        exercise_runner.auto_seed(record)
    except Exception as exc:
        findings.append(
            Finding(
                "warning",
                "Seed pack could not be loaded",
                str(exc),
                f"{record.seed_domain} phase {record.seed_phase}",
                "Lab hygiene",
            )
        )

    try:
        correct, diff, _timings = exercise_runner.check_answer_with_timing(
            record,
            answer_path=answer_path,
            timing=True,
        )
    except Exception as exc:
        correct = False
        diff = str(exc)
    check_signals, check_findings = query.compare_correctness(
        correct,
        diff,
        pointer=_relative(answer_path),
    )
    signals.extend(check_signals)
    findings.extend(check_findings)

    if request.mode == "full" and answer_path.is_file() and record.solution_path.suffix == ".sql":
        try:
            from pgfound.lab import explain

            reference_plan = explain.explain_sql(record.solution_path.read_text(encoding="utf-8"))
            learner_plan = explain.explain_sql(answer_path.read_text(encoding="utf-8"))
            plan_diff = query.diff_plans(reference_plan, learner_plan)
            plan_diffs.append(plan_diff)
            plan_signals, plan_findings = query.plan_signals(
                plan_diff, pointer=_relative(answer_path)
            )
            signals.extend(plan_signals)
            findings.extend(plan_findings)
        except Exception as exc:
            findings.append(
                Finding(
                    "warning",
                    "Plan comparison skipped",
                    str(exc),
                    _relative(answer_path),
                    "Plan evidence",
                )
            )

    rubric = grading.load_rubric(str(record.data["rubric_id"]))
    dimensions, overall, passed = grading.evaluate_rubric(rubric, signals)
    result = EvaluationResult(
        target_id=record.id,
        target_kind="exercise",
        rubric_id=str(rubric["id"]),
        dimensions=dimensions,
        overall_score=overall,
        passed=passed,
        findings=tuple(findings),
        signals=tuple(signals),
        plan_diffs=tuple(plan_diffs),
    )
    result = _write_reports(result, "exercise", record.id)
    if request.mode == "full":
        prompt_path = _render_exercise_prompt(result, record, answer_path)
        if prompt_path:
            result = _with_report_paths(result, {"prompt": _relative(prompt_path)})
    return result


def evaluate_capstone(request: EvaluationRequest) -> EvaluationResult:
    """Run the capstone review flow using deterministic artifact checks."""
    capstone_dir = paths.CAPSTONES_DIR / request.target_id
    capstone_json = capstone_dir / "capstone.json"
    if not capstone_json.is_file():
        msg = f"capstone {request.target_id!r} not found"
        raise ValueError(msg)
    capstone = json.loads(capstone_json.read_text(encoding="utf-8"))
    artifact_dir = request.artifact_path

    findings: list[Finding] = []
    signals: list[Signal] = []
    for relative in ("schema.sql", "indexes.sql", "rls-policies.sql"):
        path = artifact_dir / relative
        if relative == "schema.sql":
            found_signals, found_findings = schema.lint_schema(path)
            signals.extend(found_signals)
            findings.extend(found_findings)
        else:
            key = f"{relative.removesuffix('.sql').replace('-', '_')}_present"
            present = path.is_file() and bool(path.read_text(encoding="utf-8").strip())
            signals.append(
                Signal(
                    key,
                    "present" if present else "missing",
                    f"Checked {relative}.",
                    _relative(path),
                )
            )
            if not present:
                findings.append(
                    Finding(
                        "error",
                        f"{relative} missing",
                        "Required capstone artifact is absent or empty.",
                        _relative(path),
                    )
                )

    critical_path = artifact_dir / str(
        capstone.get("critical_queries_path", "critical-queries.sql")
    )
    critical_present = critical_path.is_file() and bool(
        critical_path.read_text(encoding="utf-8").strip()
    )
    signals.append(
        Signal(
            "critical_queries_present",
            "present" if critical_present else "missing",
            "Checked learner critical queries.",
            _relative(critical_path),
        )
    )
    if not critical_present:
        findings.append(
            Finding(
                "error",
                "Critical queries missing",
                "Submit critical-queries.sql for review.",
                _relative(critical_path),
                "Query Correctness: Result semantics",
            )
        )

    required_sections = list(capstone.get("writeup_required_sections", DEFAULT_CAPSTONE_SECTIONS))
    writeup_signals, writeup_findings = writeup.lint_writeup(
        artifact_dir / "writeup.md",
        required_sections=[str(section) for section in required_sections],
        minimum_words_per_section=10,
    )
    signals.extend(writeup_signals)
    findings.extend(writeup_findings)

    signals.extend(_capstone_posture_signals(artifact_dir))
    plan_diffs: list[dict[str, Any]] = []
    if request.mode == "full":
        reference_dir = capstone_dir / "reference"
        full_signals, full_findings, comparisons = capstone_runner.run_full_capstone_checks(
            learner_dir=artifact_dir,
            reference_dir=reference_dir,
            critical_queries_path=str(
                capstone.get("critical_queries_path", "critical-queries.sql")
            ),
            db_url=request.context.db_url,
        )
        signals.extend(full_signals)
        findings.extend(full_findings)
        if comparisons:
            plan_diffs.append(
                {
                    "kind": "critical_query_comparison",
                    "comparisons": comparisons,
                }
            )
    rubric = grading.load_rubric(str(capstone["review_rubric_id"]))
    dimensions, overall, passed = grading.evaluate_rubric(rubric, signals)
    result = EvaluationResult(
        target_id=str(capstone["id"]),
        target_kind="capstone",
        rubric_id=str(rubric["id"]),
        dimensions=dimensions,
        overall_score=overall,
        passed=passed,
        findings=tuple(findings),
        signals=tuple(signals),
        plan_diffs=tuple(plan_diffs),
    )
    result = _write_reports(result, "capstone", str(capstone["id"]))
    if request.mode == "full":
        prompt_paths = _render_capstone_prompts(result, capstone, artifact_dir)
        if prompt_paths:
            result = _with_report_paths(
                result, {key: _relative(path) for key, path in prompt_paths.items()}
            )
    return result


def _render_exercise_prompt(
    result: EvaluationResult,
    record: exercise_runner.ExerciseRecord,
    answer_path: Path,
) -> Path | None:
    if record.solution_path.suffix != ".sql":
        return None
    markdown_path = paths.REPO_ROOT / result.report_paths["markdown"]
    prompt_path = markdown_path.parent / "prompt.md"
    context = {
        "exercise_id": record.id,
        "learner_sql": _read_optional(answer_path),
        "reference_sql": _read_optional(record.solution_path),
        "rubric_id": result.rubric_id,
        "findings": json_output.result_to_dict(result)["findings"],
        "allowed_concepts": list(record.data.get("allowed_concepts", [])),
        "not_yet_allowed_concepts": list(record.data.get("not_yet_allowed_concepts", [])),
    }
    return llm_templates.render_template_to_path("critique/query-critique", context, prompt_path)


def _render_capstone_prompts(
    result: EvaluationResult,
    capstone: dict[str, Any],
    artifact_dir: Path,
) -> dict[str, Path]:
    markdown_path = paths.REPO_ROOT / result.report_paths["markdown"]
    directory = markdown_path.parent
    reviewer_directory = directory / markdown_path.stem
    prompts_directory = reviewer_directory / "prompts"
    capstone_id = str(capstone["id"])
    findings = json_output.result_to_dict(result)["findings"]
    engine_result = json_output.result_to_dict(result)
    allowed_concepts = list(capstone.get("allowed_concepts", []))
    not_yet_allowed_concepts = list(capstone.get("not_yet_allowed_concepts", []))
    reference_dir = paths.CAPSTONES_DIR / capstone_id / "reference"
    artifacts = {
        "schema.sql": _read_optional(artifact_dir / "schema.sql"),
        "indexes.sql": _read_optional(artifact_dir / "indexes.sql"),
        "rls-policies.sql": _read_optional(artifact_dir / "rls-policies.sql"),
        "critical-queries.sql": _read_optional(artifact_dir / "critical-queries.sql"),
        "operational-runbook.md": _read_optional(artifact_dir / "operational-runbook.md"),
        "writeup.md": _read_optional(artifact_dir / "writeup.md"),
    }
    reference_artifacts = {
        "schema.sql": _read_optional(reference_dir / "schema.sql"),
        "indexes.sql": _read_optional(reference_dir / "indexes.sql"),
        "rls-policies.sql": _read_optional(reference_dir / "rls-policies.sql"),
        "critical-queries.sql": _read_optional(reference_dir / "critical-queries.sql"),
        "operational-runbook.md": _read_optional(reference_dir / "operational-runbook.md"),
        "writeup.md": _read_optional(reference_dir / "writeup.md"),
    }
    common = {
        "capstone_id": capstone_id,
        "capstone_metadata": capstone,
        "rubric_id": result.rubric_id,
        "rubric": grading.load_rubric(result.rubric_id),
        "engine_result": engine_result,
        "findings": findings,
        "learner_artifacts": artifacts,
        "reference_artifacts": reference_artifacts,
        "allowed_concepts": allowed_concepts,
        "not_yet_allowed_concepts": not_yet_allowed_concepts,
    }
    rendered: dict[str, Path] = {}
    rendered["schema_prompt"] = llm_templates.render_template_to_path(
        "critique/schema-critique",
        {
            **common,
            "learner_schema": _read_optional(artifact_dir / "schema.sql"),
            "reference_schema": _read_optional(reference_dir / "schema.sql"),
        },
        directory / "schema-prompt.md",
    )
    rendered["index_prompt"] = llm_templates.render_template_to_path(
        "critique/index-critique",
        {
            "learner_index_plan": _read_optional(artifact_dir / "indexes.sql"),
            "workload_description": _read_optional(paths.CAPSTONES_DIR / capstone_id / "brief.md"),
            "existing_schema": _read_optional(artifact_dir / "schema.sql"),
            "query_examples": [_read_optional(artifact_dir / "critical-queries.sql")],
            "findings": findings,
            "allowed_concepts": allowed_concepts,
            "not_yet_allowed_concepts": not_yet_allowed_concepts,
        },
        directory / "index-prompt.md",
    )
    reviewer_templates = {
        "full_capstone_review_prompt": "capstone-reviewer/full-capstone-review",
        "operational_runbook_review_prompt": "capstone-reviewer/operational-runbook-review",
        "writeup_review_prompt": "capstone-reviewer/writeup-review",
        "extension_posture_review_prompt": "capstone-reviewer/extension-posture-review",
    }
    bundle_parts = ["# Capstone Reviewer Prompt Bundle", ""]
    for key, template_id in reviewer_templates.items():
        path = prompts_directory / f"{template_id.rsplit('/', 1)[1]}.md"
        rendered[key] = llm_templates.render_template_to_path(template_id, common, path)
        bundle_parts.extend(
            [
                f"## {template_id}",
                "",
                path.read_text(encoding="utf-8").rstrip(),
                "",
            ]
        )
    bundle_path = reviewer_directory / "prompt-bundle.md"
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    bundle_path.write_text("\n".join(bundle_parts).rstrip() + "\n", encoding="utf-8")
    readme_path = reviewer_directory / "README.md"
    readme_path.write_text(
        "\n".join(
            [
                "# Capstone Reviewer Prompt Bundle",
                "",
                "This directory contains provider-neutral LLM prompts rendered after the",
                "deterministic capstone review engine finished.",
                "",
                "- Send `prompt-bundle.md` to the LLM provider or CLI selected by the coach.",
                "- Individual prompts live under `prompts/` for targeted review passes.",
                "- The expected response shape is documented inside each rendered prompt.",
                "- Keep the deterministic Markdown and JSON review reports as the source of",
                "  engine findings; the LLM response is advisory coach feedback.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    rendered["prompt_bundle"] = bundle_path
    rendered["prompt_bundle_readme"] = readme_path
    return rendered


def _capstone_posture_signals(artifact_dir: Path) -> list[Signal]:
    rls_text = _read_optional(artifact_dir / "rls-policies.sql").lower()
    indexes_text = _read_optional(artifact_dir / "indexes.sql").lower()
    writeup_text = _read_optional(artifact_dir / "writeup.md").lower()
    return [
        Signal(
            "rls_policies_present",
            "present_and_strict"
            if "create policy" in rls_text and "current_setting" in rls_text
            else "missing",
            "Checked RLS policy SQL for policy and app context usage.",
            _relative(artifact_dir / "rls-policies.sql"),
        ),
        Signal(
            "indexes_present",
            "present" if "create index" in indexes_text else "missing",
            "Checked index artifact for CREATE INDEX statements.",
            _relative(artifact_dir / "indexes.sql"),
        ),
        Signal(
            "operational_runbook_present",
            "present" if (artifact_dir / "operational-runbook.md").is_file() else "missing",
            "Checked operational runbook artifact.",
            _relative(artifact_dir / "operational-runbook.md"),
        ),
        Signal(
            "not_yet_section_present",
            "present" if "not yet" in writeup_text else "missing",
            "Checked writeup for explicit not-yet posture.",
            _relative(artifact_dir / "writeup.md"),
        ),
    ]


def _write_reports(result: EvaluationResult, group: str, target_id: str) -> EvaluationResult:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    directory = (
        paths.TMP_DIR
        / "reviews"
        / (target_id if group == "exercise" else "capstone")
        / ("" if group == "exercise" else target_id)
    )
    if group == "exercise":
        directory = paths.TMP_DIR / "reviews" / target_id
    markdown_path = directory / f"{timestamp}.md"
    json_path = directory / f"{timestamp}.json"
    report_output.write_markdown(result, markdown_path)
    json_output.write_json(result, json_path)
    return EvaluationResult(
        target_id=result.target_id,
        target_kind=result.target_kind,
        rubric_id=result.rubric_id,
        dimensions=result.dimensions,
        overall_score=result.overall_score,
        passed=result.passed,
        findings=result.findings,
        signals=result.signals,
        plan_diffs=result.plan_diffs,
        report_paths={"markdown": _relative(markdown_path), "json": _relative(json_path)},
    )


def _with_report_paths(result: EvaluationResult, extra_paths: dict[str, str]) -> EvaluationResult:
    return EvaluationResult(
        target_id=result.target_id,
        target_kind=result.target_kind,
        rubric_id=result.rubric_id,
        dimensions=result.dimensions,
        overall_score=result.overall_score,
        passed=result.passed,
        findings=result.findings,
        signals=result.signals,
        plan_diffs=result.plan_diffs,
        report_paths={**result.report_paths, **extra_paths},
    )


def _read_optional(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(paths.REPO_ROOT))
    except ValueError:
        return str(path)

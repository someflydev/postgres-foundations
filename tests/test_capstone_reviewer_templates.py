import json

from pgfound import paths
from pgfound.llm import templates


def _context() -> dict[str, object]:
    capstone_id = "01-multi-tenant-saas-crm"
    capstone_dir = paths.CAPSTONES_DIR / capstone_id
    reference_dir = capstone_dir / "reference"
    artifacts = {
        path.name: path.read_text(encoding="utf-8")
        for path in sorted(reference_dir.iterdir())
        if path.is_file()
    }
    return {
        "capstone_id": capstone_id,
        "capstone_metadata": json.loads((capstone_dir / "capstone.json").read_text()),
        "learner_artifacts": artifacts,
        "reference_artifacts": artifacts,
        "engine_result": {"overall_score": 1.0, "findings": []},
        "rubric": json.loads((capstone_dir / "rubric.json").read_text()),
        "findings": [],
        "allowed_concepts": [],
        "not_yet_allowed_concepts": [],
    }


def test_capstone_reviewer_templates_render_against_reference_solution() -> None:
    context = _context()

    for template_id in (
        "capstone-reviewer/full-capstone-review",
        "capstone-reviewer/operational-runbook-review",
        "capstone-reviewer/writeup-review",
        "capstone-reviewer/extension-posture-review",
    ):
        rendered = templates.render_template(template_id, context)
        assert "Capstone" in rendered or "capstone" in rendered

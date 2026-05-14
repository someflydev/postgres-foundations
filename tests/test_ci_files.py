from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_github_actions_workflows_parse() -> None:
    workflow_dir = ROOT / ".github" / "workflows"
    workflow_paths = sorted(workflow_dir.glob("*.yml"))
    assert {path.name for path in workflow_paths} == {"ci.yml", "nightly-heavy.yml"}
    for path in workflow_paths:
        parsed = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert isinstance(parsed, dict)
        assert "jobs" in parsed


def test_pre_commit_config_references_expected_hooks() -> None:
    config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    hooks = {hook["id"] for repo in config["repos"] for hook in repo.get("hooks", [])}
    assert {
        "ruff",
        "ruff-format",
        "yamllint",
        "pgfound-content-validate",
        "pgfound-docs-check",
        "end-of-file-fixer",
        "trailing-whitespace",
        "check-added-large-files",
    } <= hooks

    local_hooks = {
        hook["id"]: hook
        for repo in config["repos"]
        if repo["repo"] == "local"
        for hook in repo["hooks"]
    }
    assert local_hooks["pgfound-content-validate"]["entry"] == (
        "scripts/precommit-content-validate.sh"
    )
    assert local_hooks["pgfound-docs-check"]["entry"] == "scripts/precommit-docs-check.sh"

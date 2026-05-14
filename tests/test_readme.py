import subprocess

from pgfound import docs as docs_checker
from pgfound import paths


def test_readme_lint_helper_passes() -> None:
    result = docs_checker.validate_readme(paths.REPO_ROOT / "README.md")
    assert result.errors == ()


def test_readme_lint_script_passes() -> None:
    result = subprocess.run(
        ["scripts/readme-lint.sh"],
        cwd=paths.REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr + result.stdout

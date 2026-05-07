from pathlib import Path

from pgfound import paths


def test_repo_root_is_true_repo_root() -> None:
    assert paths.REPO_ROOT == Path(__file__).resolve().parents[1]
    assert (paths.REPO_ROOT / "pyproject.toml").is_file()
    assert (paths.REPO_ROOT / ".prompts").is_dir()

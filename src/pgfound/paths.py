"""Canonical repository paths for pgfound."""

from pathlib import Path


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / ".prompts").is_dir():
            return candidate
    msg = "could not locate repository root containing pyproject.toml and .prompts/"
    raise RuntimeError(msg)


REPO_ROOT = _find_repo_root(Path(__file__).resolve())

CURRICULUM_DIR = REPO_ROOT / "curriculum"
LESSONS_DIR = CURRICULUM_DIR / "lessons"
EXERCISES_DIR = CURRICULUM_DIR / "exercises"
SCENARIOS_DIR = CURRICULUM_DIR / "scenarios"
CAPSTONES_DIR = CURRICULUM_DIR / "capstones"
RUBRICS_DIR = CURRICULUM_DIR / "rubrics"
SEED_DATA_DIR = REPO_ROOT / "seed-data"
DECISION_ENGINE_DIR = REPO_ROOT / "decision-engine"
DOCKER_DIR = REPO_ROOT / "docker"
LLM_PROMPTS_DIR = REPO_ROOT / "llm-prompts"


def ensure_exists(path: Path) -> Path:
    """Return path when it exists, otherwise raise a clear error."""
    if not path.exists():
        msg = f"required path is missing: {path}"
        raise FileNotFoundError(msg)
    return path

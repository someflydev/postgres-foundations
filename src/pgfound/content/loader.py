"""Filesystem content loaders."""

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from pgfound import paths


@dataclass(frozen=True)
class ContentItem:
    id: str
    title: str
    path: Path


CONTENT_DIRS: Final[dict[str, Path]] = {
    "lesson": paths.LESSONS_DIR,
    "exercise": paths.EXERCISES_DIR,
    "scenario": paths.SCENARIOS_DIR,
    "capstone": paths.CAPSTONES_DIR,
    "rubric": paths.RUBRICS_DIR,
}

CONTENT_EXTENSIONS: Final[set[str]] = {".json", ".yaml", ".yml", ".md", ".sql"}


def content_dir(kind: str) -> Path:
    try:
        return CONTENT_DIRS[kind]
    except KeyError as exc:
        valid = ", ".join(sorted(CONTENT_DIRS))
        msg = f"unknown content kind {kind!r}; expected one of: {valid}"
        raise ValueError(msg) from exc


def list_content(kind: str) -> list[ContentItem]:
    directory = content_dir(kind)
    if not directory.exists():
        return []
    items: list[ContentItem] = []
    for file_path in sorted(path for path in directory.rglob("*") if path.is_file()):
        if file_path.name.startswith(".") or file_path.suffix.lower() not in CONTENT_EXTENSIONS:
            continue
        content_id = file_path.stem
        items.append(ContentItem(id=content_id, title=content_id.replace("-", " "), path=file_path))
    return items


def load_raw_content(kind: str, content_id: str) -> tuple[Path, str] | None:
    directory = content_dir(kind)
    if not directory.exists():
        return None
    for file_path in sorted(path for path in directory.rglob("*") if path.is_file()):
        if file_path.stem == content_id and file_path.suffix.lower() in CONTENT_EXTENSIONS:
            return file_path, file_path.read_text(encoding="utf-8")
    return None

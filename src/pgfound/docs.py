"""Documentation validation helpers."""

from __future__ import annotations

import argparse
import re
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path

from pgfound import paths

MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)#][^)]*)\)")
FENCED_BLOCK_RE = re.compile(r"```([a-zA-Z0-9_-]*)\n(.*?)\n```", re.DOTALL)
INLINE_PATH_RE = re.compile(r"`([^`\n]*(?:/|\.md|\.json|\.sh|Makefile|LICENSE)[^`\n]*)`")


@dataclass(frozen=True)
class CheckResult:
    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.errors


def _strip_anchor(target: str) -> str:
    return target.split("#", 1)[0].strip()


def _is_external(target: str) -> bool:
    return "://" in target or target.startswith(("mailto:", "tel:"))


def _resolve_link(source_path: Path, target: str) -> Path | None:
    target = _strip_anchor(target.split()[0])
    if not target or _is_external(target):
        return None
    if target.startswith("/"):
        resolved = paths.REPO_ROOT / target.lstrip("/")
    else:
        resolved = source_path.parent / target
    return resolved.resolve()


def _normalize_existing_target(resolved: Path) -> Path:
    if resolved.is_dir():
        return resolved / "README.md"
    return resolved


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(paths.REPO_ROOT))
    except ValueError:
        return str(path)


def validate_markdown_links(root: Path) -> CheckResult:
    """Validate local markdown links under root."""
    errors: list[str] = []
    linked_docs: set[Path] = set()
    markdown_files = sorted(root.rglob("*.md"))

    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        for link in MD_LINK_RE.findall(text):
            resolved = _resolve_link(path, link)
            if resolved is None:
                continue
            candidate = _normalize_existing_target(resolved)
            if not resolved.exists() and not candidate.exists():
                errors.append(f"{_display_path(path)}: broken link target {link}")
                continue
            if candidate.suffix == ".md" and root in candidate.parents:
                linked_docs.add(candidate.resolve())

    warnings = [
        f"{_display_path(path)} is not linked from another docs page"
        for path in markdown_files
        if path.name != "README.md" and path.resolve() not in linked_docs
    ]
    return CheckResult(errors=tuple(errors), warnings=tuple(warnings))


def _readme_local_links(readme_path: Path) -> list[str]:
    text = readme_path.read_text(encoding="utf-8")
    errors: list[str] = []
    for link in MD_LINK_RE.findall(text):
        resolved = _resolve_link(readme_path, link)
        if resolved is None:
            continue
        candidate = _normalize_existing_target(resolved)
        if not resolved.exists() and not candidate.exists():
            errors.append(f"README.md: broken link target {link}")
    return errors


def _readme_inline_paths(readme_path: Path) -> list[str]:
    text = readme_path.read_text(encoding="utf-8")
    errors: list[str] = []
    for token in INLINE_PATH_RE.findall(text):
        candidate_text = token.strip()
        if candidate_text.startswith(("http://", "https://")):
            continue
        if candidate_text.startswith(("uv ", "docker ", "pgfound ", "make ", "git ")):
            continue
        candidate_text = candidate_text.removesuffix("/")
        candidate = paths.REPO_ROOT / candidate_text
        if not candidate.exists():
            errors.append(f"README.md: named path does not exist: {token}")
    return errors


def _readme_shell_blocks(readme_path: Path) -> list[str]:
    text = readme_path.read_text(encoding="utf-8")
    errors: list[str] = []
    for block_number, (language, body) in enumerate(FENCED_BLOCK_RE.findall(text), start=1):
        if language not in {"bash", "sh", "shell"}:
            continue
        for line_number, raw_line in enumerate(body.splitlines(), start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                shlex.split(line)
            except ValueError as exc:
                errors.append(
                    "README.md: shell block "
                    f"{block_number} line {line_number} does not parse: {exc}"
                )
    return errors


def validate_readme(readme_path: Path | None = None) -> CheckResult:
    """Validate the top-level README without executing its commands."""
    readme_path = readme_path or paths.REPO_ROOT / "README.md"
    if not readme_path.is_file():
        return CheckResult(errors=("README.md is missing",))
    errors = [
        *_readme_local_links(readme_path),
        *_readme_inline_paths(readme_path),
        *_readme_shell_blocks(readme_path),
    ]
    return CheckResult(errors=tuple(errors))


def _print_result(result: CheckResult) -> None:
    for warning in result.warnings:
        print(f"warning: {warning}")
    for error in result.errors:
        print(f"error: {error}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate pgfound documentation.")
    parser.add_argument("target", choices=["docs", "readme"])
    args = parser.parse_args(argv)

    if args.target == "docs":
        result = validate_markdown_links(paths.REPO_ROOT / "docs")
    else:
        result = validate_readme()

    _print_result(result)
    if result.ok:
        print("ok")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

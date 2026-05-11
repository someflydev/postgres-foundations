"""Interview transcript persistence and validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from pgfound import paths
from pgfound.interview.scenario import InterviewScenario

STAGE_RE = re.compile(r"^## Stage: (?P<kind>[a-z0-9_-]+)$", re.MULTILINE)
REQUIRED_STAGE_SECTIONS = ("### Prompt", "### Learner response", "### Simulator notes")


@dataclass(frozen=True)
class TranscriptStage:
    """Parsed transcript stage."""

    kind: str
    prompt: str
    learner_response: str
    simulator_notes: str


@dataclass(frozen=True)
class Transcript:
    """Parsed interview transcript."""

    path: Path
    scenario_id: str
    title: str
    started_at: str
    completed_at: str
    learner: str
    persona_prompt: str
    stages: tuple[TranscriptStage, ...]
    raw_text: str


def transcript_path(scenario_id: str, *, now: datetime | None = None) -> Path:
    """Return a timestamped transcript path for a scenario."""

    timestamp = (now or datetime.now(timezone.utc)).strftime("%Y%m%dT%H%M%SZ")
    return paths.TMP_DIR / "interviews" / scenario_id / f"{timestamp}.md"


def write_transcript(
    path: Path,
    *,
    scenario: InterviewScenario,
    started_at: str,
    completed_at: str,
    learner: str,
    persona_prompt: str = "",
    stages: list[dict[str, str]],
) -> Path:
    """Write a strict Markdown interview transcript."""

    lines = [
        f"# Interview: {scenario.title}",
        f"- scenario_id: {scenario.id}",
        f"- started_at: {started_at}",
        f"- completed_at: {completed_at}",
        f"- learner: {learner}",
        "",
    ]
    if persona_prompt.strip():
        lines.extend(
            [
                "## Persona Prompt",
                persona_prompt.rstrip(),
                "",
            ]
        )
    for stage in stages:
        lines.extend(
            [
                f"## Stage: {stage['kind']}",
                "### Prompt",
                stage["prompt"].rstrip(),
                "### Learner response",
                stage["learner_response"].rstrip() or "[no response recorded]",
                "### Simulator notes",
                stage["simulator_notes"].rstrip(),
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    validate_transcript(path)
    return path


def validate_transcript(path: Path) -> Transcript:
    """Parse and validate the strict interview transcript shape."""

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# Interview: "):
        msg = "transcript must start with '# Interview: <title>'"
        raise ValueError(msg)
    header = _header_values(lines[:5])
    for key in ("scenario_id", "started_at", "completed_at", "learner"):
        if key not in header or not header[key]:
            msg = f"transcript header missing {key}"
            raise ValueError(msg)

    stages = _parse_stages(text)
    if not stages:
        msg = "transcript must contain at least one stage"
        raise ValueError(msg)
    return Transcript(
        path=path,
        scenario_id=header["scenario_id"],
        title=lines[0].removeprefix("# Interview: ").strip(),
        started_at=header["started_at"],
        completed_at=header["completed_at"],
        learner=header["learner"],
        persona_prompt=_persona_prompt(text),
        stages=tuple(stages),
        raw_text=text,
    )


def _header_values(lines: list[str]) -> dict[str, str]:
    values = {}
    for line in lines[1:]:
        if not line.startswith("- ") or ": " not in line:
            continue
        key, value = line[2:].split(": ", 1)
        values[key] = value.strip()
    return values


def _parse_stages(text: str) -> list[TranscriptStage]:
    matches = list(STAGE_RE.finditer(text))
    stages = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.end() : end]
        for section in REQUIRED_STAGE_SECTIONS:
            if section not in block:
                msg = f"stage {match.group('kind')} missing {section}"
                raise ValueError(msg)
        prompt = _section(block, "### Prompt", "### Learner response")
        response = _section(block, "### Learner response", "### Simulator notes")
        notes = block.split("### Simulator notes", 1)[1].strip()
        stages.append(
            TranscriptStage(
                kind=match.group("kind"),
                prompt=prompt,
                learner_response=response,
                simulator_notes=notes,
            )
        )
    return stages


def _persona_prompt(text: str) -> str:
    marker = "## Persona Prompt"
    first_stage = "\n## Stage: "
    if marker not in text:
        return ""
    tail = text.split(marker, 1)[1]
    if first_stage in tail:
        tail = tail.split(first_stage, 1)[0]
    return tail.strip()


def _section(block: str, start: str, stop: str) -> str:
    return block.split(start, 1)[1].split(stop, 1)[0].strip()

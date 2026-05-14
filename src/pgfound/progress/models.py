"""Progress tracking data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

ModuleStatus = Literal["not-started", "in-progress", "met"]


@dataclass(frozen=True)
class LearnerProfile:
    name: str
    started_at: str
    goals: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LearnerProfile":
        return cls(
            name=str(data["name"]),
            started_at=str(data["started_at"]),
            goals=tuple(str(item) for item in data.get("goals", [])),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "started_at": self.started_at, "goals": list(self.goals)}


@dataclass(frozen=True)
class ExerciseAttempt:
    exercise_id: str
    started_at: str
    completed_at: str | None = None
    self_assessment: str = "not_recorded"
    check_result: str = "not_run"
    rubric_scores: dict[str, int | float] = field(default_factory=dict)
    notes: str = ""

    @classmethod
    def from_dict(cls, exercise_id: str, data: dict[str, Any]) -> "ExerciseAttempt":
        scores = data.get("rubric_scores", {})
        if not isinstance(scores, dict):
            raise ValueError("rubric_scores must be an object")
        return cls(
            exercise_id=exercise_id,
            started_at=str(data["started_at"]),
            completed_at=str(data["completed_at"]) if data.get("completed_at") else None,
            self_assessment=str(data.get("self_assessment", "not_recorded")),
            check_result=str(data.get("check_result", "not_run")),
            rubric_scores={str(key): _numeric(value) for key, value in scores.items()},
            notes=str(data.get("notes", "")),
        )

    def to_attempt_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "self_assessment": self.self_assessment,
            "check_result": self.check_result,
            "notes": self.notes,
        }
        if self.rubric_scores:
            payload["rubric_scores"] = self.rubric_scores
        return payload


@dataclass(frozen=True)
class CapstoneAttempt:
    capstone_id: str
    started_at: str | None = None
    completed_at: str | None = None
    workspace: str | None = None
    status: str = "started"
    rubric_scores: dict[str, int | float] = field(default_factory=dict)
    notes: str = ""

    @classmethod
    def from_dict(cls, capstone_id: str, data: dict[str, Any]) -> "CapstoneAttempt":
        scores = data.get("rubric_scores", {})
        if not isinstance(scores, dict):
            raise ValueError("rubric_scores must be an object")
        return cls(
            capstone_id=capstone_id,
            started_at=str(data["started_at"]) if data.get("started_at") else None,
            completed_at=str(data["completed_at"]) if data.get("completed_at") else None,
            workspace=str(data["workspace"]) if data.get("workspace") else None,
            status=str(data.get("status", "started")),
            rubric_scores={str(key): _numeric(value) for key, value in scores.items()},
            notes=str(data.get("notes", "")),
        )


@dataclass(frozen=True)
class InterviewAttempt:
    scenario_id: str
    transcript_path: str
    rubric_scores: dict[str, int | float]
    completed_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InterviewAttempt":
        scores = data.get("rubric_scores", {})
        if not isinstance(scores, dict):
            raise ValueError("rubric_scores must be an object")
        return cls(
            scenario_id=str(data["scenario_id"]),
            transcript_path=str(data["transcript_path"]),
            rubric_scores={str(key): _numeric(value) for key, value in scores.items()},
            completed_at=str(data["completed_at"]),
        )


@dataclass(frozen=True)
class ModuleProgress:
    module_id: str
    status: ModuleStatus
    first_touched_at: str | None = None
    exit_met_at: str | None = None
    evidence: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "module_id": self.module_id,
            "status": self.status,
            "first_touched_at": self.first_touched_at,
            "exit_met_at": self.exit_met_at,
            "evidence": list(self.evidence),
        }


def _numeric(value: Any) -> int | float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError("rubric score values must be numeric")
    return value

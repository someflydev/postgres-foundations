"""Placeholder content models expanded by later prompts."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Lesson:
    id: str
    title: str


@dataclass(frozen=True)
class Exercise:
    id: str
    title: str


@dataclass(frozen=True)
class Rubric:
    id: str
    title: str


@dataclass(frozen=True)
class Scenario:
    id: str
    title: str


@dataclass(frozen=True)
class Capstone:
    id: str
    title: str

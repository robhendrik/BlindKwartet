"""Immutable public events used by Game and full-game replay."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QuestionEvent:
    asker: int
    target: int
    category: int
    card: int


@dataclass(frozen=True)
class AnswerEvent:
    asker: int
    target: int
    category: int
    card: int
    yes: bool


@dataclass(frozen=True)
class QuartetEvent:
    player: int
    category: int


GameEvent = QuestionEvent | AnswerEvent | QuartetEvent

__all__ = ["AnswerEvent", "GameEvent", "QuestionEvent", "QuartetEvent"]

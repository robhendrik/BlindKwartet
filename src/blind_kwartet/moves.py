"""Typed pure-search actions for Blind Kwartet."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QuestionMove:
    """Ask ``target`` for one card in a category."""

    target: int
    category: int
    card: int


@dataclass(frozen=True)
class AnswerMove:
    """Answer a pending question with YES or NO."""

    yes: bool


YES = AnswerMove(True)
NO = AnswerMove(False)


@dataclass(frozen=True)
class QuartetMove:
    """Declare a quartet in a category."""

    category: int


Action = QuestionMove | AnswerMove | QuartetMove
Move = Action

__all__ = [
    "Action",
    "AnswerMove",
    "Move",
    "NO",
    "QuestionMove",
    "QuartetMove",
    "YES",
]

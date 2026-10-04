"""Public and canonical game events."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RawQuestion:
    """Question using the human names spoken in the game."""

    asker: int
    target: int
    category_name: str
    card_name: str


@dataclass(frozen=True)
class Question:
    """Canonical question after name mapping.

    Player numbers are 1-based. Category and card indices are 0-based.
    """

    asker: int
    target: int
    category: int
    card: int


@dataclass(frozen=True)
class Answer:
    """YES or NO answer to the currently pending question."""

    yes: bool


@dataclass(frozen=True)
class QuartetDeclaration:
    """A player publicly declares a complete category."""

    player: int
    category_name: str


@dataclass(frozen=True)
class CompletedQuartet:
    """Recorded completed category."""

    player: int
    category: int

"""Results returned by a completed or safely interrupted game."""

from __future__ import annotations

from dataclasses import dataclass

from .history import GameEvent
from .search_state import SearchState


@dataclass(frozen=True)
class GameResult:
    final_state: SearchState
    seat_scores: tuple[int, ...]
    winner_seats: tuple[int, ...]
    n_events: int
    end_reason: str
    seed: int | None
    history: tuple[GameEvent, ...]

    @property
    def scores(self) -> tuple[int, ...]:
        return self.seat_scores

    @property
    def is_complete(self) -> bool:
        return self.end_reason == "terminal"


__all__ = ["GameResult"]

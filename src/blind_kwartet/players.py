"""Player interfaces and simple player implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
import random
from dataclasses import dataclass

from .history import GameEvent
from .moves import Action, Move
from .search_state import SearchState


@dataclass(frozen=True)
class PlayerView:
    """Read-only information supplied to a player for one decision."""

    player_id: int
    state: SearchState
    legal_actions: tuple[Action, ...]
    history: tuple[GameEvent, ...] = ()

    @property
    def legal_moves(self) -> tuple[Action, ...]:
        return self.legal_actions


class Player(ABC):
    """Common strategy interface; legality remains owned by Game/referees."""

    @abstractmethod
    def play(self, view: PlayerView) -> Move:
        """Choose one action from ``view.legal_actions``."""


class RandomPlayer(Player):
    """Choose uniformly from the actions supplied by Game."""

    def __init__(
        self,
        seed: int | None = None,
        *,
        rng: random.Random | None = None,
    ) -> None:
        if rng is not None and seed is not None:
            raise ValueError("provide seed or rng, not both")
        self.rng = rng if rng is not None else random.Random(seed)

    def play(self, view: PlayerView) -> Move:
        if not view.legal_actions:
            raise ValueError("cannot choose from an empty action list")
        return self.rng.choice(view.legal_actions)


__all__ = ["Player", "PlayerView", "RandomPlayer"]

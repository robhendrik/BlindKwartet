"""Exact adversarial search for one four-card category.

This module is deliberately independent of the player and state-view APIs.  It
operates on a bitmap of possible *current* ownership worlds only.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


N_PLAYERS = 3
N_CARDS = 4
N_WORLDS = N_PLAYERS ** N_CARDS


class CategoryOutcome(Enum):
    """Outcome from P1's perspective."""

    WIN = "WIN"
    OPEN = "OPEN"
    LOSS = "LOSS"


WIN = CategoryOutcome.WIN
OPEN = CategoryOutcome.OPEN
LOSS = CategoryOutcome.LOSS


@dataclass(frozen=True)
class CategoryResult:
    outcome: CategoryOutcome


@dataclass(frozen=True)
class LocalCategoryMove:
    """A local ask; the asker is the recursive state's actor."""

    respondent: int
    card: int


def encode_world(owners: tuple[int, int, int, int]) -> int:
    """Encode A1..A4 owners as a base-three world index."""
    if len(owners) != N_CARDS or any(owner not in range(N_PLAYERS) for owner in owners):
        raise ValueError("owners must contain four values in range(3)")
    return sum(owner * (N_PLAYERS**card) for card, owner in enumerate(owners))


def decode_world(index: int) -> tuple[int, int, int, int]:
    """Decode a world index into A1..A4 owners."""
    if index not in range(N_WORLDS):
        raise ValueError("world index must be in range(81)")
    owners = []
    for _ in range(N_CARDS):
        index, owner = divmod(index, N_PLAYERS)
        owners.append(owner)
    return tuple(owners)  # type: ignore[return-value]


def world_bit(owners: tuple[int, int, int, int]) -> int:
    return 1 << encode_world(owners)


class SingleCategorySolver:
    """Solve a category using exact minimax recursion with path cycle checks."""

    def __init__(self) -> None:
        self.memo: dict[tuple[int, int], CategoryResult] = {}
        self.nodes = 0
        self.memo_hits = 0
        self.cycle_hits = 0
        self._stack: set[tuple[int, int]] = set()

    def solve(self, bitmap: int, actor: int = 0) -> CategoryResult:
        self._validate_state(bitmap, actor)
        return self._solve(bitmap, actor)

    def evaluate_move(
        self,
        bitmap: int,
        actor: int,
        move: LocalCategoryMove,
    ) -> CategoryResult:
        """Evaluate one ask, ignoring answer branches impossible in ``bitmap``."""
        self._validate_state(bitmap, actor)
        if move.respondent not in range(N_PLAYERS) or move.respondent == actor:
            raise ValueError("respondent must be a different local player")
        if move.card not in range(N_CARDS):
            raise ValueError("card must be in range(4)")
        return self._evaluate_move(bitmap, actor, move)

    def _solve(self, bitmap: int, actor: int) -> CategoryResult:
        key = (bitmap, actor)
        if key in self._stack:
            self.cycle_hits += 1
            return CategoryResult(OPEN)
        cached = self.memo.get(key)
        if cached is not None:
            self.memo_hits += 1
            return cached

        self.nodes += 1
        terminal = self._terminal_result(bitmap)
        if terminal is not None:
            self.memo[key] = terminal
            return terminal

        self._stack.add(key)
        try:
            moves = self._legal_moves(bitmap, actor)
            if not moves:
                result = CategoryResult(OPEN)
            else:
                results = [self._evaluate_move(bitmap, actor, move) for move in moves]
                result = self._best(results) if actor == 0 else self._worst(results)
        finally:
            self._stack.remove(key)
        self.memo[key] = result
        return result

    def _evaluate_move(
        self, bitmap: int, actor: int, move: LocalCategoryMove
    ) -> CategoryResult:
        questioned = self._legal_question_bitmap(bitmap, actor, move)
        if not questioned:
            raise ValueError("move is not legal in any world")

        yes_bitmap = 0
        no_bitmap = 0
        for index in self._set_bits(questioned):
            owners = decode_world(index)
            if owners[move.card] == move.respondent:
                updated = list(owners)
                updated[move.card] = actor
                yes_bitmap |= world_bit(tuple(updated))  # type: ignore[arg-type]
            else:
                no_bitmap |= 1 << index

        branches: list[CategoryResult] = []
        if yes_bitmap:
            branches.append(self._solve(yes_bitmap, actor))
        if no_bitmap:
            branches.append(self._solve(no_bitmap, move.respondent))
        return self._worst(branches)

    def _legal_moves(self, bitmap: int, actor: int) -> tuple[LocalCategoryMove, ...]:
        return tuple(
            LocalCategoryMove(respondent, card)
            for respondent in range(N_PLAYERS)
            if respondent != actor
            for card in range(N_CARDS)
            if self._legal_question_bitmap(
                bitmap, actor, LocalCategoryMove(respondent, card)
            )
        )

    @staticmethod
    def _legal_question_bitmap(
        bitmap: int, actor: int, move: LocalCategoryMove
    ) -> int:
        surviving = 0
        for index in SingleCategorySolver._set_bits(bitmap):
            owners = decode_world(index)
            if actor in owners and owners[move.card] != actor:
                surviving |= 1 << index
        return surviving

    @staticmethod
    def _terminal_result(bitmap: int) -> CategoryResult | None:
        if not bitmap:
            return CategoryResult(OPEN)
        worlds = [decode_world(index) for index in SingleCategorySolver._set_bits(bitmap)]
        terminal_holders = {owners[0] for owners in worlds if len(set(owners)) == 1}
        if len(terminal_holders) == 1 and len(terminal_holders) == len(worlds):
            holder = next(iter(terminal_holders))
            return CategoryResult(WIN if holder == 0 else LOSS)
        return None

    @staticmethod
    def _best(results: list[CategoryResult]) -> CategoryResult:
        return max(results, key=lambda result: _RANK[result.outcome])

    @staticmethod
    def _worst(results: list[CategoryResult]) -> CategoryResult:
        return min(results, key=lambda result: _RANK[result.outcome])

    @staticmethod
    def _set_bits(bitmap: int):
        while bitmap:
            low = bitmap & -bitmap
            yield low.bit_length() - 1
            bitmap ^= low

    @staticmethod
    def _validate_state(bitmap: int, actor: int) -> None:
        if bitmap < 0 or bitmap.bit_length() > N_WORLDS:
            raise ValueError("bitmap must contain only the 81 world bits")
        if actor not in range(N_PLAYERS):
            raise ValueError("actor must be 0, 1, or 2")


_RANK = {CategoryOutcome.LOSS: 0, CategoryOutcome.OPEN: 1, CategoryOutcome.WIN: 2}


__all__ = [
    "CategoryOutcome",
    "CategoryResult",
    "LocalCategoryMove",
    "LOSS",
    "N_CARDS",
    "N_PLAYERS",
    "N_WORLDS",
    "OPEN",
    "SingleCategorySolver",
    "WIN",
    "decode_world",
    "encode_world",
    "world_bit",
]

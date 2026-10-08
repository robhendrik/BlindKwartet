"""Measurement-only diagnostics for exact global-search state duplication.

The recorder deliberately keeps the complete ``(D, T, actor)`` values as
dictionary keys.  Compact IDs and display strings are derived only for human
readability and are never used for equality.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import random
from typing import Any

from .deals import CARDS_PER_CATEGORY, N_CATEGORIES, N_PLAYERS
from .moves import QuartetMove, QuestionMove
from .search_state import SearchState

SearchStateKey = tuple[int, tuple[int, ...], int]
SearchSubproblemKey = tuple[int, tuple[int, ...], int, int]


class GlobalSearchCutoff(RuntimeError):
    """Raised only when a diagnostic node/time limit interrupts a search."""


def exact_state_key(state: SearchState) -> SearchStateKey:
    return (state.D, state.T, state.actor)


def search_key(state: SearchState, depth_remaining: int) -> SearchSubproblemKey:
    d, t, actor = exact_state_key(state)
    return (d, t, actor, depth_remaining)


def compact_t(t: tuple[int, ...]) -> str:
    """Compact complete T representation: ``-`` is NO_OVERRIDE, else 0..2."""
    return "".join("-" if owner == -1 else str(owner) for owner in t)


def _bucket(count: int) -> str:
    if count == 1:
        return "visited once"
    if count == 2:
        return "visited twice"
    if count <= 5:
        return "visited 3-5 times"
    if count <= 10:
        return "visited 6-10 times"
    return "visited >10 times"


@dataclass(frozen=True)
class RepeatedState:
    state_id: int
    visits: int
    actors: tuple[int, ...]
    depth_remaining: tuple[int, ...]
    d_size: int
    packed_t: str


class GlobalDuplicateRecorder:
    """Collect exact state and state+depth multiplicities without memoizing."""

    def __init__(self) -> None:
        self.state_visits: Counter[SearchStateKey] = Counter()
        self.search_visits: Counter[SearchSubproblemKey] = Counter()
        self.by_depth: defaultdict[int, Counter[SearchStateKey]] = defaultdict(Counter)
        self.search_by_depth: defaultdict[int, Counter[SearchSubproblemKey]] = defaultdict(Counter)
        self._state_ids: dict[SearchStateKey, int] = {}
        self._state_meta: dict[SearchStateKey, tuple[set[int], set[int]]] = {}

    def record(self, state: SearchState, depth_remaining: int) -> None:
        key = exact_state_key(state)
        subkey = search_key(state, depth_remaining)
        self.state_visits[key] += 1
        self.search_visits[subkey] += 1
        self.by_depth[depth_remaining][key] += 1
        self.search_by_depth[depth_remaining][subkey] += 1
        if key not in self._state_ids:
            self._state_ids[key] = len(self._state_ids) + 1
            self._state_meta[key] = ({state.actor}, {depth_remaining})
        else:
            actors, depths = self._state_meta[key]
            actors.add(state.actor)
            depths.add(depth_remaining)

    @staticmethod
    def _summary(counter: Counter) -> dict[str, Any]:
        total = sum(counter.values())
        unique = len(counter)
        return {
            "total_visits": total,
            "unique": unique,
            "repeated_visits": total - unique,
            "duplicate_percentage": (100 * (total - unique) / total) if total else 0.0,
        }

    def summary(self) -> dict[str, Any]:
        return {
            "states": self._summary(self.state_visits),
            "state_depth": self._summary(self.search_visits),
            "by_depth": {
                depth: {
                    "states": self._summary(counter),
                    "state_depth": self._summary(self.search_by_depth[depth]),
                }
                for depth, counter in sorted(self.by_depth.items(), reverse=True)
            },
            "multiplicity": Counter(_bucket(count) for count in self.state_visits.values()),
            "state_depth_multiplicity": Counter(
                _bucket(count) for count in self.search_visits.values()
            ),
        }

    def top_repeated(self, limit: int = 10) -> tuple[RepeatedState, ...]:
        result = []
        for key, visits in sorted(
            ((key, visits) for key, visits in self.state_visits.items() if visits > 1),
            key=lambda item: (-item[1], item[0]),
        )[:limit]:
            d, t, actor = key
            actors, depths = self._state_meta[key]
            result.append(
                RepeatedState(
                    self._state_ids[key], visits, tuple(sorted(actors)),
                    tuple(sorted(depths)), d.bit_count(), compact_t(t),
                )
            )
        return tuple(result)


def sample_global_tree(
    samples: int,
    depth: int,
    *,
    seed: int = 123,
    initial: SearchState | None = None,
) -> tuple[GlobalDuplicateRecorder, int]:
    """Randomly sample legal stable-state paths, recording every visited state."""
    if samples < 0 or depth < 0:
        raise ValueError("samples and depth must be non-negative")
    rng = random.Random(seed)
    recorder = GlobalDuplicateRecorder()
    initial = SearchState.initial() if initial is None else initial.resolve_forced_quartets()
    for _ in range(samples):
        state = initial
        remaining = depth
        while True:
            recorder.record(state, remaining)
            if remaining == 0 or state.is_terminal:
                break
            state = _random_legal_successor(state, rng)
            if state is None:
                break
            remaining -= 1
    return recorder, samples


def _random_legal_successor(state: SearchState, rng: random.Random) -> SearchState | None:
    """Find a random legal action cheaply, while using real rule validation.

    Exhaustively constructing ``legal_moves`` is intentionally the fallback:
    the exact reference implementation checks every candidate against the
    full deal mask, which is useful for search but unnecessarily costly for a
    random sampler that only needs one legal transition.
    """
    for _ in range(64):
        if rng.random() < 0.1:
            candidate = QuartetMove(rng.randrange(N_CATEGORIES))
        else:
            category = rng.randrange(N_CATEGORIES)
            target = rng.randrange(N_PLAYERS - 1)
            if target >= state.actor:
                target += 1
            card = category * CARDS_PER_CATEGORY + rng.randrange(CARDS_PER_CATEGORY)
            candidate = QuestionMove(target, category, card)
        try:
            if isinstance(candidate, QuartetMove):
                return state.apply_quartet(candidate).resolve_forced_quartets()
            context = state.apply_question(candidate)
            answer = rng.choice(context.legal_answers())
            return context.apply_answer(answer).resolve_forced_quartets()
        except ValueError:
            continue

    actions = state.legal_moves()
    if not actions:
        return None
    action = rng.choice(actions)
    if isinstance(action, QuartetMove):
        return state.apply_quartet(action).resolve_forced_quartets()
    context = state.apply_question(action)
    return context.apply_answer(rng.choice(context.legal_answers())).resolve_forced_quartets()

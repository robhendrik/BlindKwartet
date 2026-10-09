"""Measurement-only diagnostics for exact global-search state duplication.

The recorder deliberately keeps the complete ``(D, T, actor)`` values as
dictionary keys.  Compact IDs and display strings are derived only for human
readability and are never used for equality.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import random
from time import perf_counter
from typing import Any

from .deals import CARDS_PER_CATEGORY, N_CATEGORIES, N_PLAYERS
from .moves import QuartetMove, QuestionMove
from .search_state import SearchState
from .search.canonical import canonical_key
from .compressed_search_key import (
    CompressedSearchKey,
    compressed_search_key,
    compressed_validation,
)

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

    def __init__(self, *, canonical_sample: int | None = None,
                 canonical_depth: int | None = None,
                 compressed_key_sample: int | None = 0,
                 compressed_key_depth: int | None = None) -> None:
        if canonical_sample is not None and canonical_sample < 0:
            raise ValueError("canonical_sample must be non-negative")
        self.canonical_sample = canonical_sample
        self.canonical_depth = canonical_depth
        if compressed_key_sample is not None and compressed_key_sample < 0:
            raise ValueError("compressed_key_sample must be non-negative")
        self.compressed_key_sample = compressed_key_sample
        self.compressed_key_depth = compressed_key_depth
        self.state_visits: Counter[SearchStateKey] = Counter()
        self.search_visits: Counter[SearchSubproblemKey] = Counter()
        self.by_depth: defaultdict[int, Counter[SearchStateKey]] = defaultdict(Counter)
        self.search_by_depth: defaultdict[int, Counter[SearchSubproblemKey]] = defaultdict(Counter)
        self._state_ids: dict[SearchStateKey, int] = {}
        self._state_meta: dict[SearchStateKey, tuple[set[int], set[int]]] = {}
        self.canonical_by_state: dict[SearchStateKey, tuple[int, int]] = {}
        self.canonical_representatives: dict[tuple[int, int], SearchStateKey] = {}
        self.canonical_ids: dict[tuple[int, int], int] = {}
        self.canonical_by_depth: defaultdict[int, set[tuple[int, int]]] = defaultdict(set)
        self.canonicalization_seconds = 0.0
        self.canonicalization_times: list[float] = []
        self.leaf_evaluation_seconds = 0.0
        self.leaf_evaluations = 0
        self.compressed_by_state: dict[SearchStateKey, CompressedSearchKey] = {}
        self.compressed_representatives: dict[CompressedSearchKey, SearchStateKey] = {}
        self.compressed_by_depth: defaultdict[int, set[CompressedSearchKey]] = defaultdict(set)
        self.compressed_times: list[float] = []
        self.compressed_collision_states: defaultdict[CompressedSearchKey, set[SearchStateKey]] = defaultdict(set)
        self.compressed_validation_failures = 0

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
        if key not in self.canonical_by_state and (
            (self.canonical_depth is None or depth_remaining == self.canonical_depth)
            and (
            self.canonical_sample is None
            or len(self.canonical_by_state) < self.canonical_sample
            )
        ):
            started = perf_counter()
            symmetry_key = canonical_key(state)
            elapsed = perf_counter() - started
            self.canonicalization_seconds += elapsed
            self.canonicalization_times.append(elapsed)
            self.canonical_by_state[key] = symmetry_key
            if symmetry_key not in self.canonical_representatives:
                self.canonical_representatives[symmetry_key] = key
                self.canonical_ids[symmetry_key] = len(self.canonical_ids) + 1
        symmetry_key = self.canonical_by_state.get(key)
        if symmetry_key is not None:
            self.canonical_by_depth[depth_remaining].add(symmetry_key)
        if key not in self.compressed_by_state and (
            (self.compressed_key_depth is None or depth_remaining == self.compressed_key_depth)
            and (
                self.compressed_key_sample is None
                or len(self.compressed_by_state) < self.compressed_key_sample
            )
        ):
            started = perf_counter()
            compressed = compressed_search_key(state)
            self.compressed_times.append(perf_counter() - started)
            self.compressed_by_state[key] = compressed
            self.compressed_representatives.setdefault(compressed, key)
            validation = compressed_validation(state)
            if not all(
                validation[name]
                for name in (
                    "candidate_hall_consistent",
                    "transfer_markers_consistent",
                    "authoritative_worlds_positive",
                )
            ):
                self.compressed_validation_failures += 1
        compressed = self.compressed_by_state.get(key)
        if compressed is not None:
            self.compressed_by_depth[depth_remaining].add(compressed)
            self.compressed_collision_states[compressed].add(key)

    def record_leaf_cost(self, elapsed: float) -> None:
        self.leaf_evaluation_seconds += elapsed
        self.leaf_evaluations += 1

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
        canonical_sampled = self.canonical_sample is not None
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
            "symmetry": {
                "sample_limit": self.canonical_sample,
                "sample_depth": self.canonical_depth,
                "sampled_exact_states": len(self.canonical_by_state),
                "unique_canonical": len(self.canonical_representatives),
                "by_depth": {
                    depth: len(keys)
                    for depth, keys in sorted(self.canonical_by_depth.items(), reverse=True)
                },
                "orbit_multiplicity": Counter(
                    _bucket(sum(1 for key in self.canonical_by_state.values() if key == canonical))
                    for canonical in self.canonical_representatives
                ),
                "canonicalization_seconds": self.canonicalization_seconds,
                "canonicalization_mean_ms": (
                    1000 * self.canonicalization_seconds / len(self.canonicalization_times)
                    if self.canonicalization_times else 0.0
                ),
                "canonicalization_median_ms": (
                    1000 * sorted(self.canonicalization_times)[len(self.canonicalization_times) // 2]
                    if self.canonicalization_times else 0.0
                ),
                "leaf_evaluations": self.leaf_evaluations,
                "leaf_seconds": self.leaf_evaluation_seconds,
                "leaf_mean_ms": (
                    1000 * self.leaf_evaluation_seconds / self.leaf_evaluations
                    if self.leaf_evaluations else 0.0
                ),
                "sampled": canonical_sampled,
            },
            "compressed": {
                "sample_limit": self.compressed_key_sample,
                "sample_depth": self.compressed_key_depth,
                "sampled_exact_states": len(self.compressed_by_state),
                "unique_keys": len(self.compressed_representatives),
                "by_depth": {
                    depth: len(keys)
                    for depth, keys in sorted(self.compressed_by_depth.items(), reverse=True)
                },
                "total_seconds": sum(self.compressed_times),
                "mean_ms": (
                    1000 * sum(self.compressed_times) / len(self.compressed_times)
                    if self.compressed_times else 0.0
                ),
                "median_ms": (
                    1000 * sorted(self.compressed_times)[len(self.compressed_times) // 2]
                    if self.compressed_times else 0.0
                ),
                "collision_classes": sum(
                    len(keys) > 1 for keys in self.compressed_collision_states.values()
                ),
                "validation_failures": self.compressed_validation_failures,
                "cross_category_world_correlations_encoded": False,
                "largest_classes": tuple(sorted(
                    ((len(keys), representative[0].bit_count(), compact_t(representative[1]))
                     for compressed, keys in self.compressed_collision_states.items()
                     if len(keys) > 1
                     for representative in [self.compressed_representatives[compressed]]),
                    reverse=True,
                )[:10]),
            },
        }

    def top_canonical_classes(self, limit: int = 10) -> tuple[tuple[int, int, int, str], ...]:
        counts = Counter(self.canonical_by_state.values())
        rows = []
        for canonical, count in counts.most_common(limit):
            d, _ = canonical
            rows.append((self.canonical_ids[canonical], count, d.bit_count(), compact_t(self.canonical_representatives[canonical][1])))
        return tuple(rows)

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

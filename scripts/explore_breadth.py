"""Breadth-first exploration of the pure stable SearchState graph.

One edge is one complete strategic transition: a question plus one legal
answer branch, or one quartet declaration.  The reported entropy is
``log2(|D|)`` under a uniform prior over surviving initial deals.  It is
uncertainty about the surviving initial-deal set, not strategic entropy.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import log2
from statistics import mean
from typing import Callable, Literal
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from blind_kwartet.moves import QuartetMove, QuestionMove
from blind_kwartet.search import canonical_key
from blind_kwartet.search_state import SearchState

DedupMode = Literal["raw", "canonical"]


@dataclass(frozen=True)
class GenerationReport:
    depth: int
    frontier_nodes: int
    newly_discovered: int
    cumulative_unique: int
    terminal_states: int
    raw_successors_generated: int
    canonical_unique_retained: int | None
    average_branching_factor: float
    deals_min: int
    deals_mean: float
    deals_max: int
    entropy_min: float
    entropy_mean: float
    entropy_max: float
    actions_min: int
    actions_mean: float
    actions_max: int


@dataclass(frozen=True)
class ExplorationResult:
    reports: tuple[GenerationReport, ...]
    states_by_depth: tuple[tuple[SearchState, ...], ...]
    visited_count: int
    raw_successors_generated: int
    canonical_unique_states_retained: int | None


def _state_key(state: SearchState, dedup: DedupMode):
    if dedup == "raw":
        return state
    if dedup == "canonical":
        return canonical_key(state)
    raise ValueError(f"unknown dedup mode: {dedup}")


def successors(state: SearchState, actions=None):
    """Yield ``(action, answer, stable_successor)`` edges from one state."""
    for action in state.legal_moves() if actions is None else actions:
        if isinstance(action, QuestionMove):
            context = state.apply_question(action)
            for answer in context.legal_answers():
                yield action, answer, context.apply_answer(answer)
        elif isinstance(action, QuartetMove):
            yield action, None, state.apply_quartet(action)
        else:  # pragma: no cover - legal_moves only returns these two types
            raise TypeError(f"unsupported stable action: {action!r}")


def _summary(values: list[float]) -> tuple[float, float, float]:
    return min(values), mean(values), max(values)


def _print_nodes(
    states: tuple[SearchState, ...], show_nodes: int, emit: Callable[[str], None]
) -> None:
    for index, state in enumerate(states[:show_nodes], start=1):
        actions = state.legal_moves()
        suffix = ""
        if state.is_terminal or len(state.resolved_categories) >= 2:
            suffix = f" scores={state.quartet_scores} resolved={sorted(state.resolved_categories)}"
        emit(
            f"  node {index}: actor=P{state.actor + 1} |D|={state.D.bit_count()} "
            f"uncertainty entropy={log2(state.D.bit_count()):.6f} bits "
            f"legal_actions={len(actions)}{suffix}"
        )


def _report_line(
    report: GenerationReport, dedup: DedupMode, emit: Callable[[str], None]
) -> None:
    retained = "-" if report.canonical_unique_retained is None else str(
        report.canonical_unique_retained
    )
    emit(
        f"{report.depth:5d} {report.frontier_nodes:9d} "
        f"{report.newly_discovered:11d} {report.cumulative_unique:10d} "
        f"{report.terminal_states:9d} {report.raw_successors_generated:10d} "
        f"{retained:10s} {report.average_branching_factor:7.2f} "
        f"D={report.deals_min}/{report.deals_mean:.2f}/{report.deals_max} "
        f"H={report.entropy_min:.3f}/{report.entropy_mean:.3f}/{report.entropy_max:.3f} "
        f"A={report.actions_min}/{report.actions_mean:.2f}/{report.actions_max}"
    )


def explore(
    *,
    max_depth: int,
    dedup: DedupMode = "raw",
    show_nodes: int = 0,
    initial: SearchState | None = None,
    emit: Callable[[str], None] | None = print,
) -> ExplorationResult:
    """Explore stable states breadth-first and optionally print reports."""
    if max_depth < 0:
        raise ValueError("max_depth must be non-negative")
    if show_nodes < 0:
        raise ValueError("show_nodes must be non-negative")
    if dedup not in {"raw", "canonical"}:
        raise ValueError(f"unknown dedup mode: {dedup}")
    if emit is None:
        emit = lambda _line: None

    if emit is not None:
        root = (initial or SearchState.initial()).resolve_forced_quartets()
        root_key = _state_key(root, dedup)
        visited = {root_key}
        frontier = (root,)
        states_by_depth: list[tuple[SearchState, ...]] = [frontier]
        reports: list[GenerationReport] = []
        raw_total = 0
        canonical_total: int | None = 1 if dedup == "canonical" else None

        if emit is not None:
            emit(f"BFS SearchState exploration; dedup={dedup}; max_depth={max_depth}")
            emit("Entropy is log2(|D|) under a uniform surviving-initial-deal prior.")
            emit("depth frontier newly cumulative terminal raw_edges canonical_retained "
                 "branching D(min/mean/max) H(min/mean/max) actions(min/mean/max)")

        for depth in range(max_depth + 1):
            deal_counts = [state.D.bit_count() for state in frontier]
            entropies = [log2(count) for count in deal_counts]
            action_lists = [state.legal_moves() for state in frontier]
            action_counts = [len(actions) for actions in action_lists]
            terminal_count = sum(state.is_terminal for state in frontier)
            if depth == max_depth:
                raw_edges = 0
                next_frontier: tuple[SearchState, ...] = ()
                newly = 1 if depth == 0 else 0
            else:
                candidates: list[SearchState] = []
                for state, actions in zip(frontier, action_lists):
                    candidates.extend(
                        successor for _, _, successor in successors(state, actions)
                    )
                raw_edges = len(candidates)
                raw_total += raw_edges
                next_states: list[SearchState] = []
                for candidate in candidates:
                    key = _state_key(candidate, dedup)
                    if key not in visited:
                        visited.add(key)
                        next_states.append(candidate)
                next_frontier = tuple(next_states)
                newly = len(next_frontier)
                if dedup == "canonical":
                    canonical_total = len(visited)

            deals_min, deals_mean, deals_max = _summary(deal_counts)
            entropy_min, entropy_mean, entropy_max = _summary(entropies)
            actions_min, actions_mean, actions_max = _summary(action_counts)
            report = GenerationReport(
                depth=depth,
                frontier_nodes=len(frontier),
                newly_discovered=newly,
                cumulative_unique=len(visited),
                terminal_states=terminal_count,
                raw_successors_generated=raw_edges,
                canonical_unique_retained=(
                    len(visited) if dedup == "canonical" else None
                ),
                average_branching_factor=(raw_edges / len(frontier) if frontier else 0.0),
                deals_min=int(deals_min),
                deals_mean=deals_mean,
                deals_max=int(deals_max),
                entropy_min=entropy_min,
                entropy_mean=entropy_mean,
                entropy_max=entropy_max,
                actions_min=int(actions_min),
                actions_mean=actions_mean,
                actions_max=int(actions_max),
            )
            reports.append(report)
            if emit is not None:
                _report_line(report, dedup, emit)
                if show_nodes:
                    _print_nodes(frontier, show_nodes, emit)
            if depth < max_depth:
                frontier = next_frontier
                states_by_depth.append(frontier)

        return ExplorationResult(
            reports=tuple(reports),
            states_by_depth=tuple(states_by_depth),
            visited_count=len(visited),
            raw_successors_generated=raw_total,
            canonical_unique_states_retained=canonical_total,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--dedup", choices=("raw", "canonical"), default="raw")
    parser.add_argument("--show-nodes", type=int, default=0)
    options = parser.parse_args()
    explore(
        max_depth=options.max_depth,
        dedup=options.dedup,
        show_nodes=options.show_nodes,
    )


if __name__ == "__main__":
    main()

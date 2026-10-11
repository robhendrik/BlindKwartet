"""Profile the existing exact global n-ply search.

This is measurement-only: it uses the same search entry points as the normal
benchmark and does not alter search semantics or implementation behavior.

Examples::

    PYTHONPATH=src:. python scripts/profile_global_search.py --depth 3
    PYTHONPATH=src:. python scripts/profile_global_search.py --depth 3 --include-depth-4
    PYTHONPATH=src:. python scripts/profile_global_search.py --depth 3 --memo off
"""

from __future__ import annotations

import argparse
import cProfile
from dataclasses import dataclass
from pathlib import Path
import pstats
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from blind_kwartet.players import _GlobalSearch
from blind_kwartet.search_state import SearchState
from blind_kwartet.single_category_solver import SingleCategorySolver


@dataclass(frozen=True)
class ProfileResult:
    label: str
    depth: int
    memo_enabled: bool
    selected_move: object
    returned_value: object
    nodes_expanded: int
    leaf_evaluations: int
    memo_hits: int
    memo_entries: int
    runtime_ms: float


def benchmark_state(label: str) -> SearchState:
    if label == "initial":
        return SearchState.initial()
    if label == "a1-no":
        return SearchState.initial().ask(0, 1, "A1").answer(0, 1, "A1", False)
    raise ValueError(f"unknown state: {label}")


def run_search(state: SearchState, depth: int, memo_enabled: bool) -> tuple[_GlobalSearch, object, object]:
    search = _GlobalSearch(SingleCategorySolver(), memo_enabled=memo_enabled)
    actions = search.search_actions(state, state.legal_moves(), depth)
    evaluations = tuple(
        (action, search.evaluate_action(state, action, depth))
        for action in actions
    )
    selected_index = max(
        range(len(evaluations)),
        key=lambda index: evaluations[index][1][state.actor],
    )
    selected, value = evaluations[selected_index]
    return search, selected, value


def _entry_name(entry: tuple[tuple[str, int, str], tuple[int, int, float, float, dict]]) -> str:
    (filename, line, function), _ = entry
    return f"{filename}:{line}({function})"


def _print_top(stats: pstats.Stats, *, sort_key: str, title: str) -> None:
    print(f"\nTop 20 by {title}")
    stats.sort_stats(sort_key).print_stats(20)


def _area_for(name: str) -> str:
    """Classify each profiler row once for approximate conceptual totals."""
    lowered = name.lower()
    if "single_category_solver.py" in lowered:
        return "SingleCategorySolver evaluation"
    if "category_projection.py" in lowered or "project_category_bitmap" in lowered:
        return "category projection"
    if (
        "deals.py" in lowered
        or "surviving_deal_ids" in lowered
        or "current_owner" in lowered
        or "_owner_mask" in lowered
        or "_quartet_mask" in lowered
    ):
        return "D filtering / bitmask operations"
    if "semantic_question_representatives" in lowered or "_searchnaming" in lowered:
        return "semantic grouping / naming"
    if "legal_questions" in lowered or "_legal_actions_for" in lowered:
        return "legal-question generation"
    if "apply_answer" in lowered or "answer_successor" in lowered:
        return "answer transitions"
    if "apply_question" in lowered or "_question_context" in lowered:
        return "question successor construction"
    if "apply_quartet" in lowered or "stabilize" in lowered or "resolve_forced" in lowered:
        return "quartet / stabilization"
    if "_memo_key" in lowered or "memo" in lowered:
        return "memo lookup / key construction"
    if "_leaf_value" in lowered:
        return "leaf evaluation"
    if "_evaluate_state" in lowered or "_evaluate_action" in lowered or "evaluate_answer_branches" in lowered:
        return "recursive global-search overhead"
    if "bit_count" in lowered or "_mask" in lowered or "_filter" in lowered:
        return "D filtering / bitmask operations"
    return "other"


def _print_areas(stats: pstats.Stats) -> None:
    totals: dict[str, list[float]] = {}
    for entry, values in stats.stats.items():
        name = _entry_name((entry, values))
        area = _area_for(name)
        row = totals.setdefault(area, [0.0, 0.0, 0.0])
        row[0] += values[2]  # self time
        row[1] += values[3]  # cumulative time
        row[2] += values[1]  # primitive+total call count
    total_runtime = stats.total_tt
    print("\nConceptual timing aggregates (rows classified once; cumulative is inclusive)")
    print("area                                      self ms   cumulative ms   self %   calls")
    for area, (self_time, cumulative, calls) in sorted(
        totals.items(), key=lambda item: item[1][1], reverse=True
    ):
        print(
            f"{area[:40]:40s} {self_time * 1000:9.1f} {cumulative * 1000:15.1f} "
            f"{100 * self_time / total_runtime if total_runtime else 0:7.1f} {int(calls):8d}"
        )


def profile_one(label: str, depth: int, memo_enabled: bool, output_dir: Path) -> None:
    state = benchmark_state(label)
    profile_path = output_dir / f"global_search_{label}_depth{depth}_memo{'on' if memo_enabled else 'off'}.prof"
    profiler = cProfile.Profile()
    started = time.perf_counter()
    profiler.enable()
    search, selected, value = run_search(state, depth, memo_enabled)
    profiler.disable()
    runtime_ms = (time.perf_counter() - started) * 1000
    profiler.dump_stats(str(profile_path))
    stats = pstats.Stats(profiler).strip_dirs()

    result = ProfileResult(
        label, depth, memo_enabled, selected, value, search.nodes_expanded,
        search.leaf_evaluations, search.memo_hits, search.memo_entries, runtime_ms,
    )
    print("\n" + "=" * 88)
    print(f"Profile: state={label} depth={depth} memo={'ON' if memo_enabled else 'OFF'}")
    print(f"prof file: {profile_path}")
    print(f"runtime_ms={result.runtime_ms:.1f} function_calls={stats.total_calls} primitive_calls={stats.prim_calls}")
    print(
        f"average_profiled_call_ms={1000 * stats.total_tt / stats.total_calls:.6f} "
        f"average_primitive_call_ms={1000 * stats.total_tt / stats.prim_calls:.6f}"
    )
    print(f"selected_move={result.selected_move!r}")
    print(f"returned_value={result.returned_value!r}")
    print(
        f"nodes_expanded={result.nodes_expanded} leaf_evaluations={result.leaf_evaluations} "
        f"memo_hits={result.memo_hits} memo_entries={result.memo_entries}"
    )
    _print_top(stats, sort_key="cumulative", title="cumulative time")
    _print_top(stats, sort_key="time", title="self time")
    _print_areas(stats)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--state", choices=("initial", "a1-no", "both"), default="both")
    parser.add_argument("--memo", choices=("on", "off"), default="on")
    parser.add_argument("--include-depth-4", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "profile-results")
    args = parser.parse_args()
    if args.depth < 1:
        parser.error("--depth must be positive")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    labels = ("initial", "a1-no") if args.state == "both" else (args.state,)
    depths = [args.depth]
    if args.include_depth_4 and 4 not in depths:
        depths.append(4)
    for label in labels:
        for depth in depths:
            profile_one(label, depth, args.memo == "on", args.output_dir)


if __name__ == "__main__":
    main()


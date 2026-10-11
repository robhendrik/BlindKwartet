"""Compare exact global-search work with memoization disabled and enabled.

Examples::

    PYTHONPATH=src:. python scripts/benchmark_global_memo.py --depth 3
    PYTHONPATH=src:. python scripts/benchmark_global_memo.py --depth 3 --include-depth-4
"""

from __future__ import annotations

import argparse
import time

from blind_kwartet.moves import Action
from blind_kwartet.players import _GlobalSearch
from blind_kwartet.search_state import SearchState
from blind_kwartet.single_category_solver import SingleCategorySolver


def run(label: str, state: SearchState, depth: int, memo_enabled: bool) -> dict[str, object]:
    search = _GlobalSearch(SingleCategorySolver(), memo_enabled=memo_enabled)
    started = time.perf_counter()
    actions = search.search_actions(state, state.legal_moves(), depth)
    values = tuple((action, search.evaluate_action(state, action, depth)) for action in actions)
    selected = max(range(len(values)), key=lambda index: values[index][1][state.actor])
    return {
        "label": label,
        "memo": memo_enabled,
        "depth": depth,
        "selected": values[selected][0],
        "value": values[selected][1],
        "candidate_values": values,
        "runtime_ms": (time.perf_counter() - started) * 1000,
        "nodes_expanded": search.nodes_expanded,
        "search_calls": search.search_calls,
        "leaf_evaluations": search.leaf_evaluations,
        "memo_hits": search.memo_hits,
        "memo_entries": search.memo_entries,
    }


def report(plain: dict[str, object], memo: dict[str, object]) -> None:
    print(f"\n{plain['label']} depth={plain['depth']}")
    for item in (plain, memo):
        print(
            f"  {'ON' if item['memo'] else 'OFF'}: runtime={item['runtime_ms']:.1f}ms "
            f"nodes={item['nodes_expanded']} calls={item['search_calls']} "
            f"leaves={item['leaf_evaluations']} hits={item['memo_hits']} "
            f"entries={item['memo_entries']}"
        )
    speedup = float(plain["runtime_ms"]) / float(memo["runtime_ms"])
    print(f"  speedup={speedup:.2f}x; exact_result={plain['selected'] == memo['selected'] and plain['value'] == memo['value']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--include-depth-4", action="store_true")
    args = parser.parse_args()
    if args.depth < 1:
        parser.error("--depth must be positive")

    scenarios = [("initial", SearchState.initial())]
    early = SearchState.initial().ask(0, 1, "A1").answer(0, 1, "A1", False)
    scenarios.append(("after P1 asks P2 A1 / NO", early))
    depths = [args.depth]
    if args.include_depth_4 and 4 not in depths:
        depths.append(4)
    for label, state in scenarios:
        for depth in depths:
            plain = run(label, state, depth, False)
            memo = run(label, state, depth, True)
            report(plain, memo)


if __name__ == "__main__":
    main()


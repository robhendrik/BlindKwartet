"""Benchmark exact category-projection backends and global-search integration."""

from __future__ import annotations

import argparse
import time

from blind_kwartet.category_projection import ProjectionDiagnostics, project_category_bitmap
from blind_kwartet.deals import INITIAL_DEALS
from blind_kwartet.players import _GlobalSearch
from blind_kwartet.search_state import NO_OVERRIDE, SearchState
from blind_kwartet.single_category_solver import SingleCategorySolver


def states() -> tuple[tuple[str, SearchState], ...]:
    initial = SearchState.initial()
    a1_no = initial.ask(0, 1, "A1").answer(0, 1, "A1", False)
    mid = initial.ask(0, 1, "A1").answer(0, 1, "A1", True)
    mid = mid.ask(0, 1, "A2").answer(0, 1, "A2", True)
    late = SearchState(1 << INITIAL_DEALS[1234].deal_id, (1, NO_OVERRIDE, 2,
        NO_OVERRIDE, 0, NO_OVERRIDE, 1, NO_OVERRIDE, 2, NO_OVERRIDE, 0, NO_OVERRIDE), 2)
    return ("initial", initial), ("a1-no", a1_no), ("mid-transfer", mid), ("late", late)


def projection_benchmark(state: SearchState, backend: str, repeats: int) -> dict[str, object]:
    diagnostics = ProjectionDiagnostics()
    start = time.perf_counter()
    result = 0
    for index in range(repeats):
        result ^= project_category_bitmap(
            state, index % 3, index % 3, backend=backend, diagnostics=diagnostics
        )
    elapsed = time.perf_counter() - start
    return {
        "bitmap": result,
        "calls": repeats,
        "seconds": elapsed,
        "us_per_call": elapsed * 1_000_000 / repeats,
        "calls_per_second": repeats / elapsed,
        "diagnostics": diagnostics,
    }


def global_benchmark(state: SearchState, label: str, backend: str, depth: int) -> dict[str, object]:
    search = _GlobalSearch(SingleCategorySolver(), projection_backend=backend)
    start = time.perf_counter()
    actions = search.search_actions(state, state.legal_moves(), depth)
    values = tuple((action, search.evaluate_action(state, action, depth)) for action in actions)
    selected_index = max(range(len(values)), key=lambda index: values[index][1][state.actor])
    elapsed = time.perf_counter() - start
    return {
        "label": label,
        "backend": backend,
        "seconds": elapsed,
        "selected": values[selected_index][0],
        "value": values[selected_index][1],
        "nodes": search.nodes_expanded,
        "leaves": search.leaf_evaluations,
        "memo_hits": search.memo_hits,
        "memo_entries": search.memo_entries,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--projection-repeats", type=int, default=20)
    parser.add_argument("--global-depth", type=int, default=3)
    parser.add_argument("--global", dest="run_global", action="store_true")
    parser.add_argument("--global-state", choices=("initial", "a1-no", "both"), default="both")
    parser.add_argument("--backends", default="python,numpy,numba")
    args = parser.parse_args()
    backends = tuple(item.strip() for item in args.backends.split(",") if item.strip())
    if args.projection_repeats < 1 or args.global_depth < 1:
        parser.error("repeat and depth values must be positive")

    print("Projection microbenchmark")
    projection_results: dict[tuple[str, str], dict[str, object]] = {}
    for label, state in states():
        print(f"\nstate={label} |D|={state.D.bit_count()}")
        reference = None
        for backend in backends:
            try:
                if backend == "numba":
                    compile_start = time.perf_counter()
                    project_category_bitmap(state, 0, 0, backend="numba")
                    compile_seconds = time.perf_counter() - compile_start
                else:
                    compile_seconds = 0.0
                result = projection_benchmark(state, backend, args.projection_repeats)
            except RuntimeError as exc:
                print(f"  {backend}: unavailable ({exc})")
                continue
            projection_results[(label, backend)] = result
            if reference is None:
                reference = result["bitmap"]
            print(
                f"  {backend}: {result['us_per_call']:.1f} us/call, "
                f"{result['calls_per_second']:.1f} calls/s, "
                f"speedup={float(projection_results[(label, 'python')]['seconds']) / result['seconds'] if (label, 'python') in projection_results else 1.0:.2f}x, "
                f"compile={compile_seconds:.3f}s, equal={result['bitmap'] == reference}"
            )
            diag = result["diagnostics"]
            print(
                f"    timing_us: enumerate={diag.enumeration_ns / result['calls'] / 1000:.1f} "
                f"owner_table={diag.owner_table_ns / result['calls'] / 1000:.1f} "
                f"override={diag.override_ns / result['calls'] / 1000:.1f} "
                f"encode={diag.encoding_ns / result['calls'] / 1000:.1f} "
                f"accumulate={diag.accumulation_ns / result['calls'] / 1000:.1f}"
            )

    if args.run_global:
        print("\nGlobal-search benchmark")
        selected_states = states()[:2] if args.global_state == "both" else tuple(
            item for item in states()[:2] if item[0] == args.global_state
        )
        for label, state in selected_states:
            results = []
            for backend in backends:
                try:
                    results.append(global_benchmark(state, label, backend, args.global_depth))
                except RuntimeError as exc:
                    print(f"  {label}/{backend}: unavailable ({exc})")
            baseline = next((item for item in results if item["backend"] == "python"), None)
            for item in results:
                speedup = float(baseline["seconds"]) / item["seconds"] if baseline else 1.0
                print(
                    f"  {label}/{item['backend']}: {item['seconds']:.3f}s "
                    f"speedup={speedup:.2f}x nodes={item['nodes']} leaves={item['leaves']} "
                    f"hits={item['memo_hits']} entries={item['memo_entries']} "
                    f"move={item['selected']!r} value={item['value']!r}"
                )


if __name__ == "__main__":
    main()


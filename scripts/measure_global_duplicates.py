"""Measure exact global-search transpositions without memoization."""

from __future__ import annotations

import argparse

from blind_kwartet.global_search_diagnostics import (
    GlobalDuplicateRecorder,
    GlobalSearchCutoff,
    sample_global_tree,
)
from blind_kwartet.players import _GlobalSearch
from blind_kwartet.search_state import SearchState
from blind_kwartet.single_category_solver import SingleCategorySolver


def _print_report(title: str, recorder: GlobalDuplicateRecorder) -> None:
    summary = recorder.summary()
    print(f"\n{title}")
    for label, stats in (("exact SearchState", summary["states"]), ("state+depth key", summary["state_depth"])):
        print(
            f"  {label}: total={stats['total_visits']} unique={stats['unique']} "
            f"repeated={stats['repeated_visits']} duplicate={stats['duplicate_percentage']:.2f}%"
        )
    print("  by depth_remaining:")
    for depth, stats in summary["by_depth"].items():
        state_stats = stats["states"]
        key_stats = stats["state_depth"]
        print(
            f"    {depth}: state {state_stats['total_visits']} visits / "
            f"{state_stats['unique']} unique / {state_stats['duplicate_percentage']:.2f}% dup; "
            f"key {key_stats['total_visits']} / {key_stats['unique']} / "
            f"{key_stats['duplicate_percentage']:.2f}% dup"
        )
    print("  multiplicity histogram:")
    for bucket, count in summary["multiplicity"].items():
        print(f"    {bucket}: {count}")
    print("  top repeated exact states:")
    for item in recorder.top_repeated():
        print(
            f"    S{item.state_id}: visits={item.visits} actors={item.actors} "
            f"depths={item.depth_remaining} |D|={item.d_size} T={item.packed_t}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--measure-global-duplicates", action="store_true")
    parser.add_argument("--global-depth", type=int, default=3)
    parser.add_argument("--global-node-limit", type=int)
    parser.add_argument("--global-time-limit", type=float)
    parser.add_argument("--sample-global-tree", type=int)
    parser.add_argument("--sample-depth", type=int, default=3)
    parser.add_argument("--seed", type=int, default=123)
    args = parser.parse_args()

    if args.measure_global_duplicates:
        recorder = GlobalDuplicateRecorder()
        search = _GlobalSearch(
            SingleCategorySolver(), diagnostics=recorder,
            node_limit=args.global_node_limit, time_limit=args.global_time_limit,
        )
        try:
            search.evaluate_state(SearchState.initial(), args.global_depth)
        except GlobalSearchCutoff:
            print("bounded real search: diagnostic cutoff reached; value discarded")
        _print_report("Experiment A: bounded real search", recorder)

    if args.sample_global_tree is not None:
        recorder, paths = sample_global_tree(
            args.sample_global_tree, args.sample_depth, seed=args.seed
        )
        print(f"\nMonte Carlo sampled paths: {paths}; seed={args.seed}")
        _print_report("Experiment B: Monte Carlo tree sampling", recorder)

    if not args.measure_global_duplicates and args.sample_global_tree is None:
        parser.error("select --measure-global-duplicates and/or --sample-global-tree")


if __name__ == "__main__":
    main()

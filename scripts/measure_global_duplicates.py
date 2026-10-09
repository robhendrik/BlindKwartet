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
    symmetry = summary["symmetry"]
    print("  symmetry compression:")
    if symmetry["sampled"]:
        print(f"    canonicalized unique exact states: {symmetry['sampled_exact_states']} (sample limit)")
    print(
        f"    total canonical classes: {symmetry['unique_canonical']} | "
        f"canonicalization total={symmetry['canonicalization_seconds']:.3f}s "
        f"mean={symmetry['canonicalization_mean_ms']:.3f}ms "
        f"median={symmetry['canonicalization_median_ms']:.3f}ms"
    )
    print("    by depth_remaining (visits / exact / canonical / exact-to-canonical):")
    for depth, stats in summary["by_depth"].items():
        exact = stats["states"]["unique"]
        canonical = symmetry["by_depth"].get(depth, 0)
        factor = exact / canonical if canonical else 0.0
        print(
            f"      {depth}: {stats['states']['total_visits']} / {exact} / "
            f"{canonical} / {factor:.3f}"
        )
    print("    orbit multiplicity:")
    for bucket, count in symmetry["orbit_multiplicity"].items():
        print(f"      {bucket}: {count}")
    print(
        f"    leaf evaluation: {symmetry['leaf_evaluations']} leaves, "
        f"total={symmetry['leaf_seconds']:.3f}s mean={symmetry['leaf_mean_ms']:.3f}ms"
    )
    if recorder.top_canonical_classes():
        print("    most compressed classes (count, representative |D|, representative T):")
        for canonical_id, count, d_size, packed_t in recorder.top_canonical_classes():
            print(f"      C{canonical_id}: count={count}, |D|={d_size}, T={packed_t}")
    compressed = summary["compressed"]
    print("  compressed Hall/notebook key:")
    if compressed["sample_limit"] is not None:
        print(
            f"    compressed-key states: {compressed['sampled_exact_states']} "
            f"(sample limit; depth={compressed['sample_depth']})"
        )
    print(
        f"    total keys={compressed['unique_keys']} "
        f"time={compressed['total_seconds']:.3f}s "
        f"mean={compressed['mean_ms']:.3f}ms "
        f"median={compressed['median_ms']:.3f}ms"
    )
    print("    by depth_remaining (visits / exact / compressed / exact-to-compressed):")
    for depth, stats in summary["by_depth"].items():
        exact = stats["states"]["unique"]
        compressed_count = compressed["by_depth"].get(depth, 0)
        factor = exact / compressed_count if compressed_count else 0.0
        print(
            f"      {depth}: {stats['states']['total_visits']} / {exact} / "
            f"{compressed_count} / {factor:.3f}"
        )
    print(f"    collision classes: {compressed['collision_classes']}")
    print(
        f"    projection validation failures: {compressed['validation_failures']} "
        f"(cross-category world correlations encoded: "
        f"{compressed['cross_category_world_correlations_encoded']})"
    )
    if compressed["largest_classes"]:
        print("    largest classes (exact count, representative |D|, T):")
        for count, d_size, packed_t in compressed["largest_classes"]:
            print(f"      {count}, |D|={d_size}, T={packed_t}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--measure-global-duplicates", action="store_true")
    parser.add_argument("--global-depth", type=int, default=3)
    parser.add_argument("--global-node-limit", type=int)
    parser.add_argument("--global-time-limit", type=float)
    parser.add_argument(
        "--canonical-sample", type=int, default=1000,
        help="canonicalize at most this many unique exact states (default: 1000; use 0 for none)",
    )
    parser.add_argument(
        "--canonical-depth", type=int,
        help="only canonicalize states at this remaining depth (useful for endpoint sampling)",
    )
    parser.add_argument(
        "--compressed-key-sample", type=int, default=1000,
        help="canonical compressed-key constructions to perform (default: 1000; use 0 for none)",
    )
    parser.add_argument(
        "--compressed-key-depth", type=int,
        help="only construct compressed keys at this remaining depth",
    )
    parser.add_argument("--sample-global-tree", type=int)
    parser.add_argument("--sample-depth", type=int, default=3)
    parser.add_argument("--seed", type=int, default=123)
    args = parser.parse_args()

    if args.measure_global_duplicates:
        recorder = GlobalDuplicateRecorder(
            canonical_sample=args.canonical_sample,
            canonical_depth=args.canonical_depth,
            compressed_key_sample=args.compressed_key_sample,
            compressed_key_depth=args.compressed_key_depth,
        )
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
        if args.canonical_depth is not None or args.canonical_sample != 1000:
            # Re-recording is unnecessary; this branch keeps sampling output
            # compatible while allowing endpoint-focused canonical diagnostics.
            sampled = GlobalDuplicateRecorder(
                canonical_sample=args.canonical_sample,
                canonical_depth=args.canonical_depth,
                compressed_key_sample=args.compressed_key_sample,
                compressed_key_depth=args.compressed_key_depth,
            )
            for key, visits in recorder.state_visits.items():
                state = SearchState(key[0], key[1], key[2])
                for depth, counter in recorder.by_depth.items():
                    if key in counter:
                        for _ in range(counter[key]):
                            sampled.record(state, depth)
            recorder = sampled
        print(f"\nMonte Carlo sampled paths: {paths}; seed={args.seed}")
        _print_report("Experiment B: Monte Carlo tree sampling", recorder)

    if not args.measure_global_duplicates and args.sample_global_tree is None:
        parser.error("select --measure-global-duplicates and/or --sample-global-tree")


if __name__ == "__main__":
    main()

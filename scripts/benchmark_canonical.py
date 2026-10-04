"""Reference versus optimized exact canonicalization timings."""

import argparse
from dataclasses import replace
from time import perf_counter

from blind_kwartet.game import Game
from blind_kwartet.players import RandomPlayer
from blind_kwartet.search import (
    actor_normalized_transforms,
    canonicalize,
    canonicalize_reference,
)
from blind_kwartet.search_state import SearchState


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include-large",
        action="store_true",
        help="also run exhaustive large-D cases; these can take a long time",
    )
    parser.add_argument(
        "--include-slow",
        action="store_true",
        help="also run sparse/endgame oracle cases that may take minutes",
    )
    options = parser.parse_args()
    game = Game(tuple(RandomPlayer(seed=100 + i) for i in range(3)), max_events=50)
    result = game.run()
    reachable_initial = Game.replay(result.history[:0])
    sparse = replace(
        SearchState.initial(),
        possible_initial_deals=(1 << 0) | (1 << 1),
    )
    candidates = (
        ("initial", SearchState.initial()),
        ("reachable-initial", reachable_initial),
        ("sparse-two-deal", sparse),
        ("reachable-small-slow", Game.replay(result.history[:20])),
    )
    cases = candidates if (options.include_large or options.include_slow) else tuple(
        (name, state) for name, state in candidates
        if name not in {"sparse-two-deal", "reachable-small-slow"}
    )
    n_transforms = len(actor_normalized_transforms(0))
    print(f"actor-normalized transforms={n_transforms}")
    if not options.include_large:
        print("large-D cases skipped; rerun with --include-large")
    for name, state in cases:
        print(f"\n{name}: |D|={state.D.bit_count()}")
        started = perf_counter()
        reference_key, _ = canonicalize_reference(state)
        reference_time = perf_counter() - started
        stats = {}
        started = perf_counter()
        optimized_key, _ = canonicalize(state, stats=stats)
        optimized_cold = perf_counter() - started
        started = perf_counter()
        warm_key, _ = canonicalize(state, stats=stats)
        optimized_warm = perf_counter() - started
        if optimized_key != reference_key or warm_key != reference_key:
            raise AssertionError("optimized key differs from reference")
        speedup = reference_time / optimized_warm if optimized_warm else float("inf")
        print(f"  reference={reference_time:.6f}s")
        print(
            f"  optimized cold={optimized_cold:.6f}s warm={optimized_warm:.6f}s "
            f"speedup={speedup:.2f}x full_transforms={stats['full_transforms']}"
        )
        print(f"  key_bits={reference_key[0].bit_length()}")


if __name__ == "__main__":
    main()

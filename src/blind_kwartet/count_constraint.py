"""Cross-category initial hand-size constraint."""

from __future__ import annotations

from collections import Counter
from itertools import product
from math import prod

from .config import GameConfig
from .state import CountTuple, GameState, generate_count_patterns, initial_count


class HandCountConstraint:
    """Propagate category count information between categories.

    Categories interact only through the initial deal:

        sum(category_count[k]) == initial_cards_per_player

    for every player.
    """

    def __init__(self, config: GameConfig) -> None:
        self.config = config
        patterns = sorted(generate_count_patterns(config))
        target = (config.initial_cards_per_player,) * config.n_players

        self.compatible_count_combinations: tuple[tuple[CountTuple, ...], ...] = tuple(
            combo
            for combo in product(patterns, repeat=config.n_categories)
            if tuple(
                sum(count[player] for count in combo)
                for player in range(config.n_players)
            )
            == target
        )

    def propagate(self, state: GameState) -> None:
        """Prune unsupported counts and worlds until reaching a fixed point."""
        while True:
            changed = False

            # A count cannot survive if no detailed world represents it.
            for category in state.categories:
                represented = {
                    initial_count(world, state.config)
                    for world in category.worlds
                }
                new_counts = category.counts & represented
                if new_counts != category.counts:
                    category.counts = new_counts
                    changed = True

            supported = [set() for _ in state.categories]

            for combo in self.compatible_count_combinations:
                if all(
                    combo[index] in state.categories[index].counts
                    for index in range(state.config.n_categories)
                ):
                    for index, count in enumerate(combo):
                        supported[index].add(count)

            for index, category in enumerate(state.categories):
                new_counts = category.counts & supported[index]
                if new_counts != category.counts:
                    category.counts = new_counts
                    changed = True

                old_len = len(category.worlds)
                category.worlds = [
                    world
                    for world in category.worlds
                    if initial_count(world, state.config) in category.counts
                ]
                if len(category.worlds) != old_len:
                    changed = True

            if not changed:
                return

    def is_consistent(self, state: GameState) -> bool:
        """Return whether at least one complete global hypothesis survives."""
        if any(not category.worlds for category in state.categories):
            return False

        return any(
            all(
                combo[index] in state.categories[index].counts
                for index in range(state.config.n_categories)
            )
            for combo in self.compatible_count_combinations
        )

    def global_hypothesis_count(self, state: GameState) -> int:
        """Count compatible detailed global hypotheses without materializing them."""
        multiplicities = [
            Counter(
                initial_count(world, state.config)
                for world in category.worlds
            )
            for category in state.categories
        ]

        total = 0
        for combo in self.compatible_count_combinations:
            if all(
                combo[index] in state.categories[index].counts
                for index in range(state.config.n_categories)
            ):
                total += prod(
                    multiplicities[index][combo[index]]
                    for index in range(state.config.n_categories)
                )

        return total

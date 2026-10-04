"""Core state representation."""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product

from .config import GameConfig
from .events import CompletedQuartet, Question

OwnerTuple = tuple[int, ...]
CountTuple = tuple[int, ...]


@dataclass(frozen=True)
class CategoryWorld:
    """One possible detailed state for one category.

    `initial[i]` and `current[i]` are the owners of canonical card i.

    The initial tuple never changes. The current tuple changes after public
    YES-transfers.
    """

    initial: OwnerTuple
    current: OwnerTuple


@dataclass
class CategoryState:
    """All surviving possibilities for one category."""

    worlds: list[CategoryWorld]
    counts: set[CountTuple]
    completed: bool = False
    scored_by: int | None = None


@dataclass
class NamingState:
    """Mapping from spoken names to canonical category/card indices."""

    category_names: dict[str, int] = field(default_factory=dict)
    card_names: dict[int, dict[str, int]] = field(default_factory=dict)


@dataclass
class GameState:
    """Complete referee state."""

    config: GameConfig
    categories: list[CategoryState]
    naming: NamingState
    turn: int
    pending_question: Question | None = None
    completed_quartets: list[CompletedQuartet] = field(default_factory=list)

    def score(self, player: int) -> int:
        """Return the number of completed categories scored by a player."""
        return sum(q.player == player for q in self.completed_quartets)

    @property
    def game_over(self) -> bool:
        """Whether all categories have been completed."""
        return all(category.completed for category in self.categories)


def initial_count(world: CategoryWorld, config: GameConfig) -> CountTuple:
    """Return initial category-card counts for all players."""
    return tuple(
        world.initial.count(player)
        for player in range(1, config.n_players + 1)
    )


def generate_category_worlds(config: GameConfig) -> list[CategoryWorld]:
    """Generate all legal detailed initial worlds for one category."""
    worlds: list[CategoryWorld] = []

    for owners in product(
        range(1, config.n_players + 1),
        repeat=config.cards_per_category,
    ):
        if (
            config.disallow_initial_complete_category
            and len(set(owners)) == 1
        ):
            continue

        owner_tuple = tuple(owners)
        worlds.append(
            CategoryWorld(
                initial=owner_tuple,
                current=owner_tuple,
            )
        )

    return worlds


def generate_count_patterns(config: GameConfig) -> set[CountTuple]:
    """Generate all count signatures represented by legal category worlds."""
    return {
        initial_count(world, config)
        for world in generate_category_worlds(config)
    }


def make_initial_state(
    config: GameConfig | None = None,
    *,
    first_player: int = 1,
) -> GameState:
    """Create a fresh factorized game state."""
    config = config or GameConfig()

    if first_player not in range(1, config.n_players + 1):
        raise ValueError("Invalid first player.")

    template_worlds = generate_category_worlds(config)
    template_counts = generate_count_patterns(config)

    categories = [
        CategoryState(
            worlds=list(template_worlds),
            counts=set(template_counts),
        )
        for _ in range(config.n_categories)
    ]

    return GameState(
        config=config,
        categories=categories,
        naming=NamingState(),
        turn=first_player,
    )

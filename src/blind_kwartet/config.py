"""Game configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    """Static Blind Kwartet game dimensions.

    The current project uses 3 players, 3 categories and 4 cards per category.
    The algorithms deliberately use the configuration rather than hard-coding
    those values, so configurations such as 4x4 can be explored later.

    There is no draw stack in this version.
    """

    n_players: int = 3
    n_categories: int = 3
    cards_per_category: int = 4
    disallow_initial_complete_category: bool = True

    def __post_init__(self) -> None:
        if self.n_players < 2:
            raise ValueError("At least two players are required.")
        if self.n_categories < 1:
            raise ValueError("At least one category is required.")
        if self.cards_per_category < 1:
            raise ValueError("A category must contain at least one card.")
        if self.total_cards % self.n_players:
            raise ValueError(
                "Without a draw stack, total cards must divide equally "
                "between the players."
            )

    @property
    def total_cards(self) -> int:
        """Total number of cards in the game."""
        return self.n_categories * self.cards_per_category

    @property
    def initial_cards_per_player(self) -> int:
        """Number of cards initially dealt to every player."""
        return self.total_cards // self.n_players

"""Quartet declarations, forced quartets and silence."""

from __future__ import annotations

from .events import CompletedQuartet
from .exceptions import IllegalEvent
from .state import GameState


def quartet_holder(current: tuple[int, ...]) -> int | None:
    """Return the owner if one player currently owns the whole category."""
    if current and len(set(current)) == 1:
        return current[0]
    return None


class QuartetReferee:
    """Own all rules related to complete categories."""

    def declare(self, state: GameState, player: int, category_index: int) -> None:
        """Process a voluntary/public quartet declaration."""
        if state.pending_question is not None:
            raise IllegalEvent("A quartet cannot be declared before answering.")
        if player not in range(1, state.config.n_players + 1):
            raise IllegalEvent("Invalid player.")

        category = state.categories[category_index]
        if category.completed:
            raise IllegalEvent("That category has already been completed.")

        category.worlds = [
            world
            for world in category.worlds
            if quartet_holder(world.current) == player
        ]
        if not category.worlds:
            raise IllegalEvent(
                f"P{player} cannot have a complete quartet in that category."
            )

        self._complete(state, player, category_index)

    def apply_silence(self, state: GameState) -> None:
        """Use the absence of a mandatory declaration as information.

        Before an ordinary new question, nobody has announced a quartet.
        Therefore every still-active world in which somebody already has a
        complete category is impossible.
        """
        for category in state.categories:
            if category.completed:
                continue
            category.worlds = [
                world
                for world in category.worlds
                if quartet_holder(world.current) is None
            ]

    def resolve_forced(self, state: GameState) -> list[CompletedQuartet]:
        """Automatically complete uniquely forced quartets."""
        completed: list[CompletedQuartet] = []

        for category_index, category in enumerate(state.categories):
            if category.completed or not category.worlds:
                continue

            holders = {quartet_holder(world.current) for world in category.worlds}
            if len(holders) == 1 and None not in holders:
                player = next(iter(holders))
                self._complete(state, player, category_index)
                completed.append(CompletedQuartet(player, category_index))

        return completed

    def _complete(self, state: GameState, player: int, category_index: int) -> None:
        category = state.categories[category_index]
        category.completed = True
        category.scored_by = player
        completed = CompletedQuartet(player=player, category=category_index)
        if completed not in state.completed_quartets:
            state.completed_quartets.append(completed)

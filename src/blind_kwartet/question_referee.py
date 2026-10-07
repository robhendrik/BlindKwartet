"""Question legality and detail-level pruning."""

from __future__ import annotations

from .events import Question
from .exceptions import IllegalEvent
from .state import GameState


class QuestionReferee:
    """Apply the rules revealed by asking a question."""

    def apply(self, state: GameState, question: Question) -> None:
        """Filter the relevant category by question legality."""
        config = state.config

        if state.pending_question is not None:
            raise IllegalEvent("The previous question has not been answered.")
        if question.asker != state.turn:
            raise IllegalEvent(
                f"It is P{state.turn}'s turn, not P{question.asker}'s."
            )
        if question.asker not in range(1, config.n_players + 1):
            raise IllegalEvent("Invalid asker.")
        if question.target not in range(1, config.n_players + 1):
            raise IllegalEvent("Invalid target.")
        if question.asker == question.target:
            raise IllegalEvent("A player cannot ask themselves.")
        if question.category not in range(config.n_categories):
            raise IllegalEvent("Invalid category.")
        if question.card not in range(config.cards_per_category):
            raise IllegalEvent("Invalid card.")

        category = state.categories[question.category]
        if category.completed:
            raise IllegalEvent("That category has already been completed.")

        surviving = [
            world
            for world in category.worlds
            if question.asker in world.current
            and world.current[question.card] != question.asker
        ]
        # Pythagoras termination rule: after normal asking constraints, the
        # target must still be able to own the requested card in at least one
        # surviving current world.  This rejects forced-NO questions.
        if not any(
            world.current[question.card] == question.target
            for world in surviving
        ):
            raise IllegalEvent(
                "The target cannot own that card in any surviving world."
            )
        category.worlds = surviving

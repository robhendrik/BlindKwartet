"""Answer consistency and public transfers."""

from __future__ import annotations

from .events import Answer, Question
from .exceptions import IllegalEvent
from .state import CategoryWorld, GameState


class AnswerReferee:
    """Apply YES/NO information and, after YES, transfer the card."""

    def filter_answer(
        self,
        state: GameState,
        question: Question,
        answer: Answer,
    ) -> None:
        """Keep only worlds compatible with the public answer."""
        category = state.categories[question.category]
        surviving = []

        for world in category.worlds:
            owner = world.current[question.card]
            if answer.yes and owner == question.target:
                surviving.append(world)
            elif not answer.yes and owner != question.target:
                surviving.append(world)

        category.worlds = surviving

    def transfer_yes(self, state: GameState, question: Question) -> None:
        """Transfer the requested card from target to asker in all survivors."""
        category = state.categories[question.category]
        transferred: list[CategoryWorld] = []

        for world in category.worlds:
            if world.current[question.card] != question.target:
                raise IllegalEvent(
                    "Internal inconsistency: YES-transfer without target ownership."
                )

            current = list(world.current)
            current[question.card] = question.asker
            transferred.append(
                CategoryWorld(
                    initial=world.initial,
                    current=tuple(current),
                )
            )

        category.worlds = transferred

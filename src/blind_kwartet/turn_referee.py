"""Turn progression."""

from __future__ import annotations

from .events import Answer, Question
from .state import GameState


class TurnReferee:
    """Update the next player after an answer."""

    def after_answer(
        self,
        state: GameState,
        question: Question,
        answer: Answer,
    ) -> None:
        """YES -> asker continues; NO -> answerer/target gets the turn."""
        state.turn = question.asker if answer.yes else question.target

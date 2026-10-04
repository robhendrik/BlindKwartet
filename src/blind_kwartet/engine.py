"""Modular Blind Kwartet referee engine."""

from __future__ import annotations

from copy import deepcopy

from .answer_referee import AnswerReferee
from .config import GameConfig
from .count_constraint import HandCountConstraint
from .events import Answer, QuartetDeclaration, Question, RawQuestion
from .exceptions import IllegalEvent
from .naming import MappingReferee
from .quartet_referee import QuartetReferee
from .question_referee import QuestionReferee
from .state import GameState, make_initial_state
from .turn_referee import TurnReferee


class GameEngine:
    """Coordinate modular referees around one shared GameState.

    Events are transactional: an illegal event raises IllegalEvent and leaves
    the previous state unchanged.
    """

    def __init__(
        self,
        config: GameConfig | None = None,
        *,
        first_player: int = 1,
    ) -> None:
        self.config = config or GameConfig()
        self.state = make_initial_state(self.config, first_player=first_player)

        self.mapping_referee = MappingReferee()
        self.question_referee = QuestionReferee()
        self.answer_referee = AnswerReferee()
        self.quartet_referee = QuartetReferee()
        self.turn_referee = TurnReferee()
        self.count_constraint = HandCountConstraint(self.config)

        self.count_constraint.propagate(self.state)
        self._ensure_consistent(self.state)

    def ask(self, raw_question: RawQuestion) -> Question:
        """Process a new human-named question."""
        working = deepcopy(self.state)

        if working.game_over:
            raise IllegalEvent("The game is already over.")
        if working.pending_question is not None:
            raise IllegalEvent("The previous question has not been answered.")

        # Asking instead of declaring a quartet is itself public information.
        self.quartet_referee.apply_silence(working)
        self.count_constraint.propagate(working)
        self._ensure_consistent(working)

        question = self.mapping_referee.resolve_question(working, raw_question)
        self.question_referee.apply(working, question)
        self.count_constraint.propagate(working)
        self._ensure_consistent(working)

        working.pending_question = question
        self.state = working
        return question

    def answer(self, answer: Answer) -> list:
        """Process the answer to the currently pending question."""
        working = deepcopy(self.state)
        question = working.pending_question
        if question is None:
            raise IllegalEvent("There is no pending question to answer.")

        self.answer_referee.filter_answer(working, question, answer)
        self.count_constraint.propagate(working)
        self._ensure_consistent(working)

        if answer.yes:
            self.answer_referee.transfer_yes(working, question)

        working.pending_question = None
        forced = self.quartet_referee.resolve_forced(working)
        self.turn_referee.after_answer(working, question, answer)

        self.state = working
        return forced

    def declare_quartet(self, declaration: QuartetDeclaration) -> int:
        """Process an explicit quartet announcement."""
        working = deepcopy(self.state)

        if working.game_over:
            raise IllegalEvent("The game is already over.")

        category = self.mapping_referee.resolve_category(
            working,
            declaration.category_name,
        )
        self.quartet_referee.declare(
            working,
            declaration.player,
            category,
        )
        self.count_constraint.propagate(working)
        self._ensure_consistent(working)

        self.state = working
        return category

    def global_hypothesis_count(self) -> int:
        """Return the number of compatible detailed global hypotheses."""
        return self.count_constraint.global_hypothesis_count(self.state)

    def category_snapshot(self) -> dict[int, tuple[int, int, bool]]:
        """Return {category: (detailed worlds, count patterns, completed)}."""
        return {
            index: (
                len(category.worlds),
                len(category.counts),
                category.completed,
            )
            for index, category in enumerate(self.state.categories)
        }

    def _ensure_consistent(self, state: GameState) -> None:
        if not self.count_constraint.is_consistent(state):
            raise IllegalEvent(
                "This event is inconsistent with every possible initial deal."
            )

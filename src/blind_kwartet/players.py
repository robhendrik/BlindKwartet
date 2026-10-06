"""Player interfaces and simple player implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
import random
from dataclasses import dataclass

from .history import GameEvent
from .category_projection import project_category_bitmap
from .deals import CARDS_PER_CATEGORY, N_CATEGORIES
from .moves import Action, AnswerMove, Move, QuestionMove, QuartetMove
from .search_state import SearchState
from .single_category_solver import (
    CategoryOutcome,
    CategoryResult,
    LocalCategoryMove,
    SingleCategorySolver,
)


@dataclass(frozen=True)
class TreeDecisionDiagnostic:
    """Diagnostics for one call made to ``SingleCategoryTreePlayer.play``."""

    action_kind: str
    supplied_questions: int
    evaluated_win: int
    evaluated_open: int
    evaluated_loss: int
    selected_outcome: CategoryOutcome | None
    selected_category: int | None
    possible_initial_deals: int
    unresolved_categories: int
    deals_collapsed: bool
    solver_nodes: int
    solver_memo_hits: int
    solver_cycle_hits: int
    category_best_values: tuple[tuple[int, CategoryOutcome], ...] = ()


@dataclass(frozen=True)
class PlayerView:
    """Read-only information supplied to a player for one decision."""

    player_id: int
    state: SearchState
    legal_actions: tuple[Action, ...]
    history: tuple[GameEvent, ...] = ()

    @property
    def legal_moves(self) -> tuple[Action, ...]:
        return self.legal_actions


class Player(ABC):
    """Common strategy interface; legality remains owned by Game/referees."""

    @abstractmethod
    def play(self, view: PlayerView) -> Move:
        """Choose one action from ``view.legal_actions``."""


class RandomPlayer(Player):
    """Choose uniformly from the actions supplied by Game."""

    def __init__(
        self,
        seed: int | None = None,
        *,
        rng: random.Random | None = None,
    ) -> None:
        if rng is not None and seed is not None:
            raise ValueError("provide seed or rng, not both")
        self.rng = rng if rng is not None else random.Random(seed)

    def play(self, view: PlayerView) -> Move:
        if not view.legal_actions:
            raise ValueError("cannot choose from an empty action list")
        return self.rng.choice(view.legal_actions)


class SingleCategoryTreePlayer(Player):
    """Choose supplied asks using exact single-category adversarial search."""

    def __init__(self) -> None:
        self.solver = SingleCategorySolver()
        self.moves_evaluated = 0
        self.win_evaluations = 0
        self.open_evaluations = 0
        self.loss_evaluations = 0
        self.last_evaluations: tuple[tuple[QuestionMove, CategoryResult], ...] = ()
        self.decision_diagnostics: list[TreeDecisionDiagnostic] = []

    @property
    def solver_nodes(self) -> int:
        return self.solver.nodes

    @property
    def solver_memo_hits(self) -> int:
        return self.solver.memo_hits

    @property
    def solver_cycle_hits(self) -> int:
        return self.solver.cycle_hits

    def play(self, view: PlayerView) -> Move:
        """Choose one of the actions supplied by the game environment."""
        legal_moves = tuple(view.legal_actions)
        if not legal_moves:
            raise ValueError("cannot choose from an empty action list")

        nodes_before = self.solver.nodes
        memo_hits_before = self.solver.memo_hits
        cycle_hits_before = self.solver.cycle_hits
        supplied_questions = sum(
            isinstance(move, QuestionMove) for move in legal_moves
        )

        def record(
            action_kind: str,
            selected_outcome: CategoryOutcome | None = None,
            selected_category: int | None = None,
            *,
            evaluated_win: int = 0,
            evaluated_open: int = 0,
            evaluated_loss: int = 0,
            category_best_values: tuple[tuple[int, CategoryOutcome], ...] = (),
        ) -> None:
            self.decision_diagnostics.append(
                TreeDecisionDiagnostic(
                    action_kind=action_kind,
                    supplied_questions=supplied_questions,
                    evaluated_win=evaluated_win,
                    evaluated_open=evaluated_open,
                    evaluated_loss=evaluated_loss,
                    selected_outcome=selected_outcome,
                    selected_category=selected_category,
                    possible_initial_deals=view.state.D.bit_count(),
                    unresolved_categories=N_CATEGORIES - len(view.state.resolved_categories),
                    deals_collapsed=view.state.D.bit_count() == 1,
                    solver_nodes=self.solver.nodes - nodes_before,
                    solver_memo_hits=self.solver.memo_hits - memo_hits_before,
                    solver_cycle_hits=self.solver.cycle_hits - cycle_hits_before,
                    category_best_values=category_best_values,
                )
            )

        quartets = [move for move in legal_moves if isinstance(move, QuartetMove)]
        if quartets:
            choice = min(quartets, key=lambda move: move.category)
            record("quartet", selected_category=choice.category)
            return choice

        answers = [move for move in legal_moves if isinstance(move, AnswerMove)]
        if answers:
            # The game currently supplies answer actions only to the target;
            # keep this player total without pretending the local ask solver
            # can evaluate a pending global question.
            choice = min(answers, key=lambda move: move.yes)
            record("answer")
            return choice

        asks = [move for move in legal_moves if isinstance(move, QuestionMove)]
        if not asks:
            raise ValueError("legal moves contain no supported action")

        evaluations = tuple(
            (move, self._evaluate_question(view, move))
            for move in sorted(asks, key=self._question_key)
        )
        self.last_evaluations = evaluations
        for _, result in evaluations:
            self.moves_evaluated += 1
            if result.outcome is CategoryOutcome.WIN:
                self.win_evaluations += 1
            elif result.outcome is CategoryOutcome.OPEN:
                self.open_evaluations += 1
            else:
                self.loss_evaluations += 1

        category_best: dict[int, CategoryOutcome] = {}
        outcome_rank = {
            CategoryOutcome.LOSS: 0,
            CategoryOutcome.OPEN: 1,
            CategoryOutcome.WIN: 2,
        }
        for move, result in evaluations:
            previous = category_best.get(move.category)
            if previous is None or outcome_rank[result.outcome] > outcome_rank[previous]:
                category_best[move.category] = result.outcome

        choice = max(
            evaluations,
            key=lambda item: outcome_rank[item[1].outcome],
        )[0]
        selected_result = next(result for move, result in evaluations if move == choice)
        record(
            "question",
            selected_outcome=selected_result.outcome,
            selected_category=choice.category,
            evaluated_win=sum(result.outcome is CategoryOutcome.WIN for _, result in evaluations),
            evaluated_open=sum(result.outcome is CategoryOutcome.OPEN for _, result in evaluations),
            evaluated_loss=sum(result.outcome is CategoryOutcome.LOSS for _, result in evaluations),
            category_best_values=tuple(sorted(category_best.items())),
        )
        return choice

    def _evaluate_question(
        self, view: PlayerView, move: QuestionMove
    ) -> CategoryResult:
        bitmap = project_category_bitmap(view.state, move.category, view.player_id)
        local_target = (move.target - view.player_id) % 3
        local_card = move.card - move.category * CARDS_PER_CATEGORY
        local_move = LocalCategoryMove(local_target, local_card)
        return self.solver.evaluate_move(bitmap, 0, local_move)

    @staticmethod
    def _question_key(move: QuestionMove) -> tuple[int, int, int]:
        # Match SearchState.legal_questions(): category, target, card.
        return move.category, move.target, move.card


__all__ = [
    "Player",
    "PlayerView",
    "RandomPlayer",
    "SingleCategoryTreePlayer",
    "TreeDecisionDiagnostic",
]

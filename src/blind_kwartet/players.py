"""Player interfaces and simple player implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
import random
from dataclasses import dataclass
import time

from .history import GameEvent, QuestionEvent
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


GlobalPlayerValue = tuple[int, int, int, int, int]
GlobalValueVector = tuple[GlobalPlayerValue, ...]


def _global_action_key(action) -> tuple[int, int, int, int]:
    if isinstance(action, QuartetMove):
        return (0, action.category, 0, 0)
    return (1, action.category, action.target, action.card)


class _GlobalSearch:
    """Small depth-limited Max-N search over stable global SearchStates."""

    def __init__(self, solver: SingleCategorySolver) -> None:
        self.solver = solver
        self.nodes_expanded = 0
        self.leaf_evaluations = 0
        self.terminal_evaluations = 0
        self.max_branching_factor = 0

    def evaluate_state(self, state: SearchState, depth: int) -> GlobalValueVector:
        self.nodes_expanded += 1
        if state.is_terminal:
            self.terminal_evaluations += 1
            return self._terminal_value(state)
        if depth <= 0:
            self.leaf_evaluations += 1
            return self._leaf_value(state)

        actions = self._ordered_actions(state.legal_moves())
        self.max_branching_factor = max(self.max_branching_factor, len(actions))
        if not actions:
            return self._leaf_value(state)
        values = [self._evaluate_action(state, action, depth) for action in actions]
        actor = state.actor
        best_index = max(
            range(len(values)),
            key=lambda index: values[index][actor],
        )
        return values[best_index]

    def evaluate_action(
        self,
        state: SearchState,
        action,
        depth: int,
    ) -> GlobalValueVector:
        return self._evaluate_action(state, action, depth)

    def evaluate_answer_branches(
        self,
        context,
        answerer: int,
        remaining_depth: int,
    ) -> tuple[AnswerMove, GlobalValueVector, GlobalValueVector | None]:
        legal_answers = context.legal_answers()
        if len(legal_answers) == 1:
            successor = self._answer_successor(context, legal_answers[0])
            value = self.evaluate_state(successor, remaining_depth)
            return legal_answers[0], value, None
        yes = self._answer_successor(context, AnswerMove(True))
        no = self._answer_successor(context, AnswerMove(False))
        yes_value = self.evaluate_state(yes, remaining_depth)
        no_value = self.evaluate_state(no, remaining_depth)
        if yes_value[answerer] > no_value[answerer]:
            return AnswerMove(True), yes_value, no_value
        return AnswerMove(False), yes_value, no_value

    def _evaluate_action(self, state: SearchState, action, depth: int) -> GlobalValueVector:
        if isinstance(action, QuartetMove):
            successor = state.apply_quartet(action).resolve_forced_quartets()
            return self.evaluate_state(successor, depth - 1)
        context = state.apply_question(action)
        answer, yes_value, no_value = self.evaluate_answer_branches(
            context,
            action.target,
            depth - 1,
        )
        # The branch values were already evaluated while selecting the
        # answer; do not expand the selected successor a second time.
        return yes_value if answer.yes else no_value  # type: ignore[return-value]

    @staticmethod
    def _answer_successor(context, answer: AnswerMove) -> SearchState:
        return context.apply_answer(answer).resolve_forced_quartets()

    def _leaf_value(self, state: SearchState) -> GlobalValueVector:
        values = []
        for player in range(3):
            wins = opens = losses = 0
            for category in range(3):
                if category in state.resolved_categories:
                    continue
                bitmap = project_category_bitmap(state, category, player)
                local_actor = (state.actor - player) % 3
                outcome = self.solver.solve(bitmap, local_actor).outcome
                if outcome is CategoryOutcome.WIN:
                    wins += 1
                elif outcome is CategoryOutcome.OPEN:
                    opens += 1
                else:
                    losses += 1
            values.append((0, state.quartet_scores[player], wins, opens, -losses))
        return tuple(values)  # type: ignore[return-value]

    @staticmethod
    def _terminal_value(state: SearchState) -> GlobalValueVector:
        scores = state.quartet_scores
        high = max(scores)
        winners = sum(score == high for score in scores)
        values = []
        for player, score in enumerate(scores):
            rank = 2 if score == high and winners == 1 else 1 if score == high else 0
            values.append((rank, score, 0, 0, 0))
        return tuple(values)  # type: ignore[return-value]

    @staticmethod
    def _ordered_actions(actions):
        return tuple(sorted(actions, key=_global_action_key))


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
    answerer: int | None = None
    answer_category: int | None = None
    answer_card: int | None = None
    answer_asker: int | None = None
    yes_outcome: CategoryOutcome | None = None
    no_outcome: CategoryOutcome | None = None
    selected_answer: bool | None = None
    answer_selection_reason: str | None = None
    global_depth: int = 0
    global_nodes_expanded: int = 0
    global_leaf_evaluations: int = 0
    global_terminal_evaluations: int = 0
    global_max_branching_factor: int = 0
    selected_global_value: GlobalPlayerValue | None = None
    competing_global_values: tuple[tuple[str, GlobalPlayerValue], ...] = ()
    global_runtime_ms: float | None = None


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

    def __init__(self, global_depth: int = 0) -> None:
        if global_depth < 0:
            raise ValueError("global_depth must be non-negative")
        self.global_depth = global_depth
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
            answerer: int | None = None,
            answer_category: int | None = None,
            answer_card: int | None = None,
            answer_asker: int | None = None,
            yes_outcome: CategoryOutcome | None = None,
            no_outcome: CategoryOutcome | None = None,
            selected_answer: bool | None = None,
            answer_selection_reason: str | None = None,
            global_search: _GlobalSearch | None = None,
            selected_global_value: GlobalPlayerValue | None = None,
            competing_global_values: tuple[tuple[str, GlobalPlayerValue], ...] = (),
            global_runtime_ms: float | None = None,
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
                    answerer=answerer,
                    answer_category=answer_category,
                    answer_card=answer_card,
                    answer_asker=answer_asker,
                    yes_outcome=yes_outcome,
                    no_outcome=no_outcome,
                    selected_answer=selected_answer,
                    answer_selection_reason=answer_selection_reason,
                    global_depth=self.global_depth,
                    global_nodes_expanded=0 if global_search is None else global_search.nodes_expanded,
                    global_leaf_evaluations=0 if global_search is None else global_search.leaf_evaluations,
                    global_terminal_evaluations=0 if global_search is None else global_search.terminal_evaluations,
                    global_max_branching_factor=0 if global_search is None else global_search.max_branching_factor,
                    selected_global_value=selected_global_value,
                    competing_global_values=competing_global_values,
                    global_runtime_ms=global_runtime_ms,
                )
            )

        quartets = [move for move in legal_moves if isinstance(move, QuartetMove)]
        if quartets and self.global_depth == 0:
            choice = min(quartets, key=lambda move: move.category)
            record("quartet", selected_category=choice.category)
            return choice

        answers = [move for move in legal_moves if isinstance(move, AnswerMove)]
        if answers:
            choice = min(answers, key=lambda move: move.yes)
            question = self._pending_question(view)
            answer_asker = view.history[-1].asker
            if len(answers) == 2:
                context = view.state.apply_question(question)
                global_search = None
                start = time.perf_counter()
                if self.global_depth > 0:
                    global_search = _GlobalSearch(self.solver)
                    choice, yes_value, no_value = global_search.evaluate_answer_branches(
                        context,
                        view.player_id,
                        self.global_depth - 1,
                    )
                    yes_result = no_result = None
                else:
                    yes_result = self._evaluate_answer_branch(
                        view, question, context, AnswerMove(True)
                    )
                    no_result = self._evaluate_answer_branch(
                        view, question, context, AnswerMove(False)
                    )
                    yes_value = no_value = None
                if self.global_depth == 0 and self._outcome_rank(yes_result) > self._outcome_rank(no_result):
                    choice = AnswerMove(True)
                    reason = "strict"
                elif self.global_depth == 0:
                    reason = "tie" if yes_result is no_result else "strict"
                else:
                    reason = "tie" if yes_value[view.player_id] == no_value[view.player_id] else "strict"
                record(
                    "answer",
                    answerer=view.player_id,
                    answer_category=question.category,
                    answer_card=question.card,
                    answer_asker=answer_asker,
                    yes_outcome=yes_result,
                    no_outcome=no_result,
                    selected_answer=choice.yes,
                    answer_selection_reason=reason,
                    global_search=global_search,
                    selected_global_value=(
                        yes_value[view.player_id] if choice.yes else no_value[view.player_id]
                    ) if self.global_depth > 0 else None,
                    competing_global_values=(
                        (("YES", yes_value[view.player_id]), ("NO", no_value[view.player_id]))
                        if self.global_depth > 0 else ()
                    ),
                    global_runtime_ms=(time.perf_counter() - start) * 1000
                    if self.global_depth > 0 else None,
                )
            else:
                record(
                    "answer",
                    answerer=view.player_id,
                    answer_category=question.category,
                    answer_card=question.card,
                    answer_asker=answer_asker,
                    selected_answer=choice.yes,
                )
            return choice

        asks = [move for move in legal_moves if isinstance(move, QuestionMove)]
        if not asks and self.global_depth == 0:
            raise ValueError("legal moves contain no supported action")

        if self.global_depth > 0:
            start = time.perf_counter()
            global_search = _GlobalSearch(self.solver)
            ordered_actions = _GlobalSearch._ordered_actions(legal_moves)
            evaluations_global = tuple(
                (
                    move,
                    global_search.evaluate_action(view.state, move, self.global_depth),
                )
                for move in ordered_actions
            )
            actor = view.player_id
            selected_index = max(
                range(len(evaluations_global)),
                key=lambda index: evaluations_global[index][1][actor],
            )
            choice = evaluations_global[selected_index][0]
            competing = tuple(
                (repr(move), value[actor]) for move, value in evaluations_global
            )
            record(
                "question" if isinstance(choice, QuestionMove) else "quartet",
                selected_category=getattr(choice, "category", None),
                global_search=global_search,
                selected_global_value=evaluations_global[selected_index][1][actor],
                competing_global_values=competing,
                global_runtime_ms=(time.perf_counter() - start) * 1000,
            )
            return choice

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

    def _evaluate_answer_branch(
        self,
        view: PlayerView,
        question: QuestionMove,
        context,
        answer: AnswerMove,
    ) -> CategoryOutcome:
        """Evaluate one answer branch from the answerer's perspective."""
        resulting_state = context.apply_answer(answer).resolve_forced_quartets()
        bitmap = project_category_bitmap(
            resulting_state, question.category, view.player_id
        )
        local_actor = (resulting_state.actor - view.player_id) % 3
        return self.solver.solve(bitmap, local_actor).outcome

    @staticmethod
    def _pending_question(view: PlayerView) -> QuestionMove:
        if not view.history or not isinstance(view.history[-1], QuestionEvent):
            raise ValueError("strategic answer evaluation requires a pending question")
        event = view.history[-1]
        return QuestionMove(event.target, event.category, event.card)

    @staticmethod
    def _outcome_rank(outcome: CategoryOutcome) -> int:
        return {
            CategoryOutcome.LOSS: 0,
            CategoryOutcome.OPEN: 1,
            CategoryOutcome.WIN: 2,
        }[outcome]

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

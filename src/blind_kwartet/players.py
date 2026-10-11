"""Player interfaces and simple player implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
import random
from dataclasses import dataclass, field
import time

from .history import GameEvent, QuestionEvent
from .category_projection import project_category_bitmap
from .deals import CARDS_PER_CATEGORY, INITIAL_OWNER_MASKS, N_CATEGORIES, N_PLAYERS
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


@dataclass(frozen=True)
class _SearchNaming:
    """Minimal search-only naming history; never part of SearchState."""

    categories: tuple[int, ...] = ()
    cards: tuple[tuple[int, ...], ...] = ((), (), ())


def _card_constraint_signature(state: SearchState, card: int) -> tuple[int, int, int]:
    initial_mask = sum(
        1 << player
        for player in range(N_PLAYERS)
        if INITIAL_OWNER_MASKS[player][card] & state.D
    )
    override = state.T[card]
    current_mask = (
        1 << override
        if override >= 0
        else initial_mask
    )
    return initial_mask, current_mask, override


def _category_constraint_signature(state: SearchState, category: int):
    start = category * CARDS_PER_CATEGORY
    cards = tuple(
        sorted(
            _card_constraint_signature(state, start + offset)
            for offset in range(CARDS_PER_CATEGORY)
        )
    )
    holder = state.quartet_holders()[category]
    return (category in state.resolved_categories, holder, cards)


def _infer_search_naming(state: SearchState) -> _SearchNaming:
    """Infer named slots from non-generic exact constraints at a search root."""
    generic = (7, 7, -1)
    categories = []
    cards = [[], [], []]
    for category in range(N_CATEGORIES):
        for offset in range(CARDS_PER_CATEGORY):
            card = category * CARDS_PER_CATEGORY + offset
            if _card_constraint_signature(state, card) != generic:
                cards[category].append(card)
                if category not in categories:
                    categories.append(category)
        if category in state.resolved_categories and category not in categories:
            categories.append(category)
    return _SearchNaming(tuple(categories), tuple(tuple(row) for row in cards))


def _advance_search_naming(
    naming: _SearchNaming, move: QuestionMove
) -> _SearchNaming:
    categories = list(naming.categories)
    cards = [list(row) for row in naming.cards]
    if move.category not in categories:
        categories.append(move.category)
    if move.card not in cards[move.category]:
        cards[move.category].append(move.card)
    return _SearchNaming(tuple(categories), tuple(tuple(row) for row in cards))


def semantic_question_representatives(
    state: SearchState,
    questions: tuple[QuestionMove, ...] | list[QuestionMove],
    naming: _SearchNaming | None = None,
) -> tuple[QuestionMove, ...]:
    """Return one exact representative for each local naming-symmetry class.

    Targets are part of the class key.  Named category/card slots are never
    exchanged with new slots; otherwise equal exact constraints are compared
    structurally, without invoking compressed keys or full-state transforms.
    """
    naming = _infer_search_naming(state) if naming is None else naming
    classes: dict[tuple[object, ...], QuestionMove] = {}
    for move in questions:
        if move.category in naming.categories:
            category_key = ("named-category", move.category)
        else:
            category_key = ("new-category", _category_constraint_signature(state, move.category))
        if move.card in naming.cards[move.category]:
            card_key = ("named-card", move.card)
        else:
            card_key = ("new-card", _card_constraint_signature(state, move.card))
        key = (move.target, category_key, card_key)
        current = classes.get(key)
        if current is None or (move.category, move.card) < (current.category, current.card):
            classes[key] = move
    return tuple(sorted(classes.values(), key=_global_action_key))


def _global_action_key(action) -> tuple[int, int, int, int]:
    if isinstance(action, QuartetMove):
        return (0, action.category, 0, 0)
    return (1, action.category, action.target, action.card)


class _GlobalSearch:
    """Small depth-limited Max-N search over stable global SearchStates."""

    def __init__(
        self,
        solver: SingleCategorySolver,
        *,
        diagnostics=None,
        node_limit: int | None = None,
        time_limit: float | None = None,
        move_symmetry_pruning: bool = True,
    ) -> None:
        if node_limit is not None and node_limit < 1:
            raise ValueError("node_limit must be positive")
        if time_limit is not None and time_limit <= 0:
            raise ValueError("time_limit must be positive")
        self.solver = solver
        self.diagnostics = diagnostics
        self.node_limit = node_limit
        self.time_limit = time_limit
        self.move_symmetry_pruning = move_symmetry_pruning
        self._started_at = time.perf_counter()
        self.nodes_expanded = 0
        self.leaf_evaluations = 0
        self.terminal_evaluations = 0
        self.max_branching_factor = 0
        self.raw_legal_questions = 0
        self.semantic_question_classes = 0
        self.pruned_equivalent_questions = 0
        self.question_branching_by_depth: dict[int, dict[str, int]] = defaultdict(
            lambda: {
                "raw_legal_questions": 0,
                "semantic_question_classes": 0,
                "pruned_equivalent_questions": 0,
            }
        )

    @property
    def branching_reduction_percent(self) -> float:
        if not self.raw_legal_questions:
            return 0.0
        return 100.0 * self.pruned_equivalent_questions / self.raw_legal_questions

    @property
    def symmetry_diagnostics(self) -> dict[str, object]:
        return {
            "raw_legal_questions": self.raw_legal_questions,
            "semantic_question_classes": self.semantic_question_classes,
            "pruned_equivalent_questions": self.pruned_equivalent_questions,
            "branching_reduction_percent": self.branching_reduction_percent,
            "by_depth": {
                depth: dict(values)
                for depth, values in sorted(self.question_branching_by_depth.items())
            },
        }

    def search_actions(
        self,
        state: SearchState,
        actions: tuple[Action, ...] | list[Action],
        depth: int = 0,
        naming: _SearchNaming | None = None,
    ) -> tuple[Action, ...]:
        """Quotient exact supplied actions for search expansion only."""
        exact_questions = tuple(action for action in actions if isinstance(action, QuestionMove))
        naming = _infer_search_naming(state) if naming is None else naming
        semantic_questions = (
            semantic_question_representatives(state, exact_questions, naming)
            if self.move_symmetry_pruning else exact_questions
        )
        raw_count = len(exact_questions)
        semantic_count = len(semantic_questions)
        pruned_count = raw_count - semantic_count
        self.raw_legal_questions += raw_count
        self.semantic_question_classes += semantic_count
        self.pruned_equivalent_questions += pruned_count
        depth_stats = self.question_branching_by_depth[depth]
        depth_stats["raw_legal_questions"] += raw_count
        depth_stats["semantic_question_classes"] += semantic_count
        depth_stats["pruned_equivalent_questions"] += pruned_count
        other_actions = tuple(action for action in actions if not isinstance(action, QuestionMove))
        return self._ordered_actions((*semantic_questions, *other_actions))

    def evaluate_state(self, state: SearchState, depth: int) -> GlobalValueVector:
        return self._evaluate_state_impl(state, depth, _infer_search_naming(state))

    def _evaluate_state_impl(
        self, state: SearchState, depth: int, naming: _SearchNaming
    ) -> GlobalValueVector:
        self.nodes_expanded += 1
        if self.diagnostics is not None:
            self.diagnostics.record(state, depth)
        if (
            self.node_limit is not None
            and self.nodes_expanded >= self.node_limit
        ) or (
            self.time_limit is not None
            and time.perf_counter() - self._started_at >= self.time_limit
        ):
            from .global_search_diagnostics import GlobalSearchCutoff

            raise GlobalSearchCutoff("diagnostic global search cutoff")
        if state.is_terminal:
            self.terminal_evaluations += 1
            return self._terminal_value(state)
        if depth <= 0:
            self.leaf_evaluations += 1
            started = time.perf_counter()
            value = self._leaf_value(state)
            if self.diagnostics is not None:
                record_leaf_cost = getattr(self.diagnostics, "record_leaf_cost", None)
                if record_leaf_cost is not None:
                    record_leaf_cost(time.perf_counter() - started)
            return value

        exact_actions = state.legal_moves()
        actions = self.search_actions(state, exact_actions, depth, naming)
        self.max_branching_factor = max(self.max_branching_factor, len(actions))
        if not actions:
            started = time.perf_counter()
            value = self._leaf_value(state)
            if self.diagnostics is not None:
                record_leaf_cost = getattr(self.diagnostics, "record_leaf_cost", None)
                if record_leaf_cost is not None:
                    record_leaf_cost(time.perf_counter() - started)
            return value
        values = [
            self._evaluate_action(
                state,
                action,
                depth,
                _advance_search_naming(naming, action)
                if isinstance(action, QuestionMove) else naming,
            )
            for action in actions
        ]
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
        return self._evaluate_action(
            state,
            action,
            depth,
            _advance_search_naming(_infer_search_naming(state), action)
            if isinstance(action, QuestionMove) else _infer_search_naming(state),
        )

    def evaluate_answer_branches(
        self,
        context,
        answerer: int,
        remaining_depth: int,
        naming: _SearchNaming | None = None,
    ) -> tuple[AnswerMove, GlobalValueVector, GlobalValueVector | None]:
        legal_answers = context.legal_answers()
        if len(legal_answers) == 1:
            successor = self._answer_successor(context, legal_answers[0])
            value = self._evaluate_state_with_naming(
                successor, remaining_depth, naming or _infer_search_naming(successor)
            )
            return legal_answers[0], value, None
        yes = self._answer_successor(context, AnswerMove(True))
        no = self._answer_successor(context, AnswerMove(False))
        active_naming = naming or _infer_search_naming(context.state)
        yes_value = self._evaluate_state_with_naming(yes, remaining_depth, active_naming)
        no_value = self._evaluate_state_with_naming(no, remaining_depth, active_naming)
        if yes_value[answerer] > no_value[answerer]:
            return AnswerMove(True), yes_value, no_value
        return AnswerMove(False), yes_value, no_value

    def _evaluate_action(
        self,
        state: SearchState,
        action,
        depth: int,
        naming: _SearchNaming,
    ) -> GlobalValueVector:
        if isinstance(action, QuartetMove):
            successor = state.apply_quartet(action).resolve_forced_quartets()
            return self._evaluate_state_with_naming(successor, depth - 1, naming)
        context = state.apply_question(action)
        answer, yes_value, no_value = self.evaluate_answer_branches(
            context,
            action.target,
            depth - 1,
            naming,
        )
        # The branch values were already evaluated while selecting the
        # answer; do not expand the selected successor a second time.
        return yes_value if answer.yes else no_value  # type: ignore[return-value]

    def _evaluate_state_with_naming(
        self, state: SearchState, depth: int, naming: _SearchNaming
    ) -> GlobalValueVector:
        """Recursive entry retaining naming metadata outside SearchState."""
        # Preserve the existing monkeypatch/test seam while retaining the
        # structured naming context on normal recursive search calls.
        patched_evaluate_state = self.__dict__.get("evaluate_state")
        if patched_evaluate_state is not None:
            return patched_evaluate_state(state, depth)
        return self._evaluate_state_impl(state, depth, naming)

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
    global_raw_legal_questions: int = 0
    global_semantic_question_classes: int = 0
    global_pruned_equivalent_questions: int = 0
    global_branching_reduction_percent: float = 0.0
    global_symmetry_by_depth: dict[int, dict[str, int]] = field(default_factory=dict)
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
                    global_raw_legal_questions=0 if global_search is None else global_search.raw_legal_questions,
                    global_semantic_question_classes=0 if global_search is None else global_search.semantic_question_classes,
                    global_pruned_equivalent_questions=0 if global_search is None else global_search.pruned_equivalent_questions,
                    global_branching_reduction_percent=0.0 if global_search is None else global_search.branching_reduction_percent,
                    global_symmetry_by_depth={} if global_search is None else global_search.symmetry_diagnostics["by_depth"],
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
            ordered_actions = global_search.search_actions(
                view.state, legal_moves, self.global_depth
            )
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

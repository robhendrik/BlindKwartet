from blind_kwartet.players import TreeDecisionDiagnostic
from blind_kwartet.single_category_solver import CategoryOutcome
from scripts.benchmark_single_category_tree import (
    best_value_pairs,
    classify_decision,
    observe_game,
)
from blind_kwartet.search_state import SearchState
from blind_kwartet.result import GameResult


def diagnostic(*, wins=0, opens=0, losses=0, values=(), unresolved=1):
    return TreeDecisionDiagnostic(
        action_kind="question",
        supplied_questions=wins + opens + losses,
        evaluated_win=wins,
        evaluated_open=opens,
        evaluated_loss=losses,
        selected_outcome=None,
        selected_category=None,
        possible_initial_deals=10,
        unresolved_categories=unresolved,
        deals_collapsed=False,
        solver_nodes=1,
        solver_memo_hits=2,
        solver_cycle_hits=3,
        category_best_values=values,
    )


def test_decision_classification_prioritizes_win_then_open_then_loss():
    assert classify_decision(diagnostic(wins=1, opens=2, losses=3)) == "at least one WIN"
    assert classify_decision(diagnostic(opens=1, losses=3)) == "no WIN but at least one OPEN"
    assert classify_decision(diagnostic(losses=3)) == "LOSS only"


def test_cross_category_value_pairs_are_detected():
    diag = diagnostic(
        values=(
            (0, CategoryOutcome.WIN),
            (1, CategoryOutcome.OPEN),
            (2, CategoryOutcome.LOSS),
        )
    )

    assert best_value_pairs(diag) == {
        "one category WIN, another OPEN",
        "one category WIN, another LOSS",
        "one category OPEN, another LOSS",
    }


def test_game_observation_records_tree_score_and_event_limit():
    result = GameResult(
        final_state=SearchState.initial(),
        seat_scores=(2, 1, 0),
        winner_seats=(),
        n_events=5,
        end_reason="event_limit",
        seed=123,
        history=(),
    )

    observation = observe_game(result, tree_seat=1)

    assert observation.tree_score == 1
    assert observation.event_limit_reached

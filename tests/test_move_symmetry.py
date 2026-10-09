from dataclasses import replace

from blind_kwartet.moves import QuestionMove
from blind_kwartet.players import (
    _GlobalSearch,
    _SearchNaming,
    semantic_question_representatives,
)
from blind_kwartet.search_state import SearchState
from blind_kwartet.single_category_solver import SingleCategorySolver


def _questions(state):
    return state.legal_questions()


def test_initial_questions_collapse_cards_categories_but_not_targets():
    state = SearchState.initial()
    representatives = semantic_question_representatives(state, _questions(state))

    assert representatives == (
        QuestionMove(1, 0, 0),
        QuestionMove(2, 0, 0),
    )


def test_after_a1_new_a_card_and_new_category_are_canonicalized():
    state = SearchState.initial().ask(0, 1, "A1").answer(0, 1, "A1", True)
    representatives = semantic_question_representatives(state, _questions(state))

    assert QuestionMove(1, 0, 1) in representatives
    assert QuestionMove(1, 0, 2) not in representatives
    assert QuestionMove(1, 1, 4) in representatives
    assert QuestionMove(1, 1, 7) not in representatives
    assert QuestionMove(2, 0, 1) in representatives
    assert QuestionMove(2, 1, 4) in representatives


def test_after_a1_a2_remaining_a3_a4_share_one_representative():
    state = SearchState.initial()
    state = state.ask(0, 1, "A1").answer(0, 1, "A1", True)
    state = state.ask(0, 1, "A2").answer(0, 1, "A2", True)
    representatives = semantic_question_representatives(state, _questions(state))

    assert QuestionMove(1, 0, 2) in representatives
    assert QuestionMove(1, 0, 3) not in representatives


def test_b1_b4_counterexample_is_one_new_category_branch():
    state = SearchState.initial()
    state = state.ask(0, 1, "A1").answer(0, 1, "A1", True)
    state = state.ask(0, 1, "A2").answer(0, 1, "A2", True)
    representatives = semantic_question_representatives(state, _questions(state))

    assert QuestionMove(2, 1, 4) in representatives
    assert QuestionMove(2, 1, 7) not in representatives


def test_distinct_card_constraints_are_not_collapsed():
    state = replace(
        SearchState.initial(),
        current_owner_override=(-1, 1) + (-1,) * 10,
    )
    questions = tuple(QuestionMove(1, 0, card) for card in range(4))
    representatives = semantic_question_representatives(state, questions)

    assert QuestionMove(1, 0, 0) in representatives
    assert QuestionMove(1, 0, 1) in representatives


def test_distinct_category_constraints_are_not_collapsed():
    state = replace(
        SearchState.initial(),
        current_owner_override=(0,) + (-1,) * 3 + (1,) + (-1,) * 7,
    )
    questions = tuple(QuestionMove(1, category, category * 4) for category in range(3))
    representatives = semantic_question_representatives(state, questions)

    assert len(representatives) == 3


def test_pruning_does_not_change_depth_one_value_with_small_stub_solver():
    state = SearchState.initial()
    plain = _GlobalSearch(SingleCategorySolver(), move_symmetry_pruning=False)
    pruned = _GlobalSearch(SingleCategorySolver(), move_symmetry_pruning=True)
    value = ((0, 0, 0, 0, 0),) * 3
    plain._leaf_value = lambda _state: value
    pruned._leaf_value = lambda _state: value

    # This isolates branch selection from the deliberately expensive
    # single-category leaf solver; production search still uses that solver.
    assert pruned.evaluate_state(state, 1) == plain.evaluate_state(state, 1)
    assert pruned.raw_legal_questions > pruned.semantic_question_classes
    assert pruned.pruned_equivalent_questions > 0
    assert pruned.branching_reduction_percent > 0


def test_pruning_is_only_at_search_boundary_and_honors_public_names():
    state = SearchState.initial()
    exact = state.legal_questions()
    search = _GlobalSearch(SingleCategorySolver())
    naming = _SearchNaming(categories=(0,), cards=((0,), (), ()))

    # The state/engine still exposes every exact labelled action.
    assert len(exact) == 24
    representatives = search.search_actions(state, exact, naming=naming)

    # A supplied public name prevents A1 from being treated as a new card,
    # while the still-unnamed cards in A remain one semantic class.
    assert QuestionMove(1, 0, 0) in representatives
    assert QuestionMove(1, 0, 1) in representatives
    assert QuestionMove(1, 0, 2) not in representatives
    assert len(representatives) == 6


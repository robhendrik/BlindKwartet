"""Focused Milestone 1.5 pure action-layer tests."""

from dataclasses import replace

import pytest

from blind_kwartet.moves import AnswerMove, QuestionMove, QuartetMove, NO, YES
from blind_kwartet.search_state import SearchInvariantError, SearchState


def test_legal_questions_are_actor_and_world_compatible():
    state = SearchState.initial()
    questions = state.legal_questions()

    assert questions
    assert all(question.target != state.actor for question in questions)
    for question in questions:
        context = state.apply_question(question)
        assert context.state.D & ~state.D == 0
        for deal_id in context.state.surviving_deal_ids():
            owners = context.state.current_owners(deal_id)
            family = owners[question.category * 4: question.category * 4 + 4]
            assert state.actor in family
            assert owners[question.card] != state.actor


def test_question_for_card_already_owned_is_illegal():
    initial = SearchState.initial()
    state = initial._filter(
        lambda deal_id: initial.current_owner(deal_id, "A1") == 0
    )
    with pytest.raises(ValueError):
        state.apply_question(QuestionMove(target=1, category=0, card=0))


def test_both_answers_are_available_and_strategic():
    context = SearchState.initial().apply_question(
        QuestionMove(target=1, category=0, card=0)
    )
    assert context.legal_answers() == (YES, NO)
    assert context.D_yes and context.D_no


def test_target_impossible_question_is_rejected_after_no():
    state = SearchState.initial().ask(0, 1, "A1").answer(0, 1, "A1", False)

    assert state.actor == 1
    with pytest.raises(ValueError, match="target cannot own"):
        state.ask(1, 0, "A1")


def test_legal_question_always_has_a_yes_branch():
    for question in SearchState.initial().legal_questions():
        context = SearchState.initial().apply_question(question)
        assert context.D_yes


def test_forced_yes_and_forced_no():
    context = SearchState.initial().apply_question(
        QuestionMove(target=1, category=0, card=0)
    )
    forced_yes = replace(context, no_mask=0).apply_answer(YES)
    forced_no = replace(context, yes_mask=0).apply_answer(NO)
    assert forced_yes.D == context.D_yes
    assert forced_yes.actor == 0
    assert forced_no.D == context.D_no
    assert forced_no.actor == 1


def test_voluntary_quartet_filters_d_and_keeps_turn():
    initial = SearchState.initial()
    overrides = (0,) + ( -1,) * 11
    state = replace(initial, current_owner_override=overrides)
    declaration = QuartetMove(category=0)

    assert declaration in state.legal_quartets()
    result = state.apply_quartet(declaration)
    assert result.D & ~state.D == 0
    assert 0 in result.resolved_categories
    assert result.actor == 0


def test_impossible_quartet_declaration_is_rejected():
    with pytest.raises(ValueError):
        SearchState.initial().apply_quartet(QuartetMove(category=0))


def test_forced_quartet_resolution_is_derived():
    initial = SearchState.initial()
    state = replace(initial, current_owner_override=(0,) + (-1,) * 11)
    mask = state._mask(
        lambda deal_id: all(
            state.current_owner(deal_id, card) == 0
            for card in range(4)
        )
    )
    forced = replace(state, possible_initial_deals=mask)
    assert forced.forced_quartets() == (QuartetMove(0),)
    resolved = forced.resolve_forced_quartets()
    assert resolved.resolved_categories == frozenset({0})
    assert resolved.quartet_scores[0] == 1


def test_terminal_score_preserves_a_true_three_way_tie():
    overrides = (0,) * 4 + (1,) * 4 + (2,) * 4
    state = replace(SearchState.initial(), current_owner_override=overrides)
    assert state.is_terminal
    assert state.quartet_scores == (1, 1, 1)
    assert state.legal_moves() == ()


def test_stabilization_skips_actor_and_reports_invariant(monkeypatch):
    state = SearchState.initial()
    monkeypatch.setattr(
        SearchState,
        "_legal_actions_for",
        lambda self, actor: (QuestionMove(0, 0, 0),) if actor == 1 else (),
    )
    assert state.stabilize(0).actor == 1

    monkeypatch.setattr(SearchState, "_legal_actions_for", lambda self, actor: ())
    with pytest.raises(SearchInvariantError):
        state.stabilize(0)


def test_d_never_grows_through_action_transitions():
    state = SearchState.initial()
    context = state.apply_question(state.legal_questions()[0])
    next_state = context.apply_answer(AnswerMove(True))
    assert context.state.D & ~state.D == 0
    assert next_state.D & ~context.state.D == 0

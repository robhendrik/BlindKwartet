from dataclasses import replace

from blind_kwartet.moves import AnswerMove, QuestionMove
from blind_kwartet.players import _GlobalSearch, _SearchNaming
from blind_kwartet.search_state import SearchState
from blind_kwartet.single_category_solver import SingleCategorySolver


def _search(state, depth, *, memo_enabled):
    search = _GlobalSearch(SingleCategorySolver(), memo_enabled=memo_enabled)
    actions = search.search_actions(state, state.legal_moves(), depth)
    evaluated = tuple((action, search.evaluate_action(state, action, depth)) for action in actions)
    selected = max(range(len(evaluated)), key=lambda index: evaluated[index][1][state.actor])
    return search, evaluated[selected], evaluated


def test_memoized_initial_depths_match_non_memoized_exactly():
    for depth in (1, 2):
        plain, selected_plain, values_plain = _search(SearchState.initial(), depth, memo_enabled=False)
        memo, selected_memo, values_memo = _search(SearchState.initial(), depth, memo_enabled=True)
        assert selected_memo == selected_plain
        assert values_memo == values_plain
        assert memo.memo_entries > 0
        if depth == 2:
            assert memo.memo_hits > 0
        assert plain.memo_entries == 0


def test_memo_key_keeps_naming_contexts_distinct():
    state = SearchState.initial()
    search = _GlobalSearch(SingleCategorySolver(), memo_enabled=True)
    value = ((0, 0, 0, 0, 0),) * 3
    search._leaf_value = lambda _state: value
    named = _SearchNaming(categories=(0,), cards=((0,), (), ()))
    unnamed = _SearchNaming()
    search._evaluate_state_impl(state, 0, named)
    search._evaluate_state_impl(state, 0, unnamed)
    assert search.memo_entries == 2
    assert search.memo_hits == 0


def test_strategic_answer_branches_match_with_and_without_memo():
    state = SearchState.initial()
    question = state.legal_questions()[0]
    context = state.apply_question(question)
    plain = _GlobalSearch(SingleCategorySolver(), memo_enabled=False)
    memo = _GlobalSearch(SingleCategorySolver(), memo_enabled=True)
    assert memo.evaluate_answer_branches(context, question.target, 2) == plain.evaluate_answer_branches(
        context, question.target, 2
    )


def test_reachable_transfer_and_resolved_states_match():
    initial = SearchState.initial()
    states = [
        initial.ask(0, 1, "A1").answer(0, 1, "A1", False),
        initial.ask(0, 1, "A1").answer(0, 1, "A1", True).ask(0, 1, "A2").answer(
            0, 1, "A2", True
        ),
        replace(initial, current_owner_override=(0,) * 4 + (-1,) * 8).resolve_forced_quartets(),
    ]
    for state in states:
        plain, selected_plain, values_plain = _search(state, 1, memo_enabled=False)
        memo, selected_memo, values_memo = _search(state, 1, memo_enabled=True)
        assert selected_memo == selected_plain
        assert values_memo == values_plain
        assert memo.memo_entries == memo.search_calls


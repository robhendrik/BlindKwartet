from dataclasses import replace

from blind_kwartet.global_search_diagnostics import (
    GlobalDuplicateRecorder,
    exact_state_key,
    sample_global_tree,
    search_key,
)
from blind_kwartet.players import _GlobalSearch
from blind_kwartet.search_state import SearchState
from blind_kwartet.single_category_solver import SingleCategorySolver


def test_identical_raw_states_are_counted_as_duplicates():
    recorder = GlobalDuplicateRecorder()
    state = SearchState.initial()
    recorder.record(state, 2)
    recorder.record(replace(state), 2)

    assert recorder.summary()["states"] == {
        "total_visits": 2,
        "unique": 1,
        "repeated_visits": 1,
        "duplicate_percentage": 50.0,
    }


def test_different_depths_share_exact_state_but_not_search_key():
    recorder = GlobalDuplicateRecorder()
    state = SearchState.initial()
    recorder.record(state, 2)
    recorder.record(state, 1)

    assert len(recorder.state_visits) == 1
    assert len(recorder.search_visits) == 2
    assert exact_state_key(state) != search_key(state, 1)


def test_different_d_t_and_actor_do_not_collide():
    base = SearchState.initial()
    variants = (
        replace(base, possible_initial_deals=base.D ^ 1),
        replace(base, current_owner_override=(0,) + base.T[1:]),
        replace(base, actor=1),
    )
    recorder = GlobalDuplicateRecorder()
    for state in (base, *variants):
        recorder.record(state, 1)
    assert len(recorder.state_visits) == 4


def test_fixed_seed_sampling_is_reproducible():
    first, paths = sample_global_tree(20, 3, seed=123)
    second, second_paths = sample_global_tree(20, 3, seed=123)
    assert paths == second_paths == 20
    assert first.state_visits == second.state_visits
    assert first.search_visits == second.search_visits


def test_diagnostics_do_not_change_normal_search_value():
    state = SearchState.initial()
    plain = _GlobalSearch(SingleCategorySolver()).evaluate_state(state, 1)
    recorder = GlobalDuplicateRecorder()
    measured = _GlobalSearch(
        SingleCategorySolver(), diagnostics=recorder
    ).evaluate_state(state, 1)
    assert measured == plain

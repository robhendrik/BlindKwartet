from blind_kwartet.category_projection import project_category_bitmap
from blind_kwartet.deals import INITIAL_DEALS
from blind_kwartet.search_state import SearchState
from blind_kwartet.single_category_solver import decode_world, world_bit


def category_owners(state, deal_id, category=0):
    start = category * 4
    return tuple(state.current_owner(deal_id, start + card) for card in range(4))


def state_with_category(category_owners_value, category=0):
    state = SearchState.initial()
    return state._filter(
        lambda deal_id: category_owners(state, deal_id, category)
        == category_owners_value
    )


def projected_worlds(bitmap):
    return {decode_world(index) for index in range(81) if bitmap & (1 << index)}


def test_fully_known_category_projects_to_one_normalized_world():
    state = state_with_category((0, 1, 2, 2))
    bitmap = project_category_bitmap(state, category=0, active_player_id=0)

    assert bitmap.bit_count() == 1
    assert projected_worlds(bitmap) == {(0, 1, 2, 2)}


def test_global_worlds_differing_elsewhere_collapse_locally():
    state = state_with_category((0, 1, 2, 2))
    assert len(state.surviving_deal_ids()) > 1

    bitmap = project_category_bitmap(state, 0, 0)

    assert projected_worlds(bitmap) == {(0, 1, 2, 2)}


def test_genuine_category_uncertainty_preserves_exact_local_world_set():
    state = SearchState.initial()
    state = state._filter(
        lambda deal_id: state.current_owner(deal_id, "A1") == 0
    )
    expected = {
        tuple(state.current_owner(deal_id, card) for card in range(4))
        for deal_id in state.surviving_deal_ids()
    }

    bitmap = project_category_bitmap(state, 0, 0)

    assert projected_worlds(bitmap) == expected
    assert bitmap == sum(world_bit(owners) for owners in expected)


def test_projection_uses_current_holder_after_transfer():
    state = state_with_category((1, 0, 2, 2))
    asked = state.ask(0, 1, "A1")
    transferred = asked.answer(0, 1, "A1", True)

    bitmap = project_category_bitmap(transferred, 0, 0)

    assert projected_worlds(bitmap) == {(0, 0, 2, 2)}
    assert all(
        INITIAL_DEALS[deal_id].owner_by_card[0] == 1
        for deal_id in transferred.surviving_deal_ids()
    )


def test_active_player_is_normalized_to_p1_without_mirroring_p2_p3():
    state = state_with_category((0, 1, 2, 2))

    assert projected_worlds(project_category_bitmap(state, 0, 0)) == {(0, 1, 2, 2)}
    assert projected_worlds(project_category_bitmap(state, 0, 1)) == {(2, 0, 1, 1)}
    assert projected_worlds(project_category_bitmap(state, 0, 2)) == {(1, 2, 0, 0)}


def test_projection_is_compatible_with_solver_encoding():
    state = state_with_category((2, 0, 1, 2))
    bitmap = project_category_bitmap(state, 0, 0)
    index = next(index for index in range(81) if bitmap & (1 << index))

    assert decode_world(index) == (2, 0, 1, 2)


def test_realistic_canonical_prefix_projects_current_ownership():
    state = SearchState.initial()
    state = state._filter(
        lambda deal_id: (
            state.current_owner(deal_id, "A1") != 0
            and 1 <= sum(state.current_owner(deal_id, card) == 0 for card in range(4)) < 4
        )
    )

    state = state.ask(0, 1, "A1").answer(0, 1, "A1", False)
    assert state.actor == 1
    state = state.ask(1, 2, "A1").answer(1, 2, "A1", True)
    state = state.ask(1, 2, "A2").answer(1, 2, "A2", False)
    state = state.ask(2, 0, "A2").answer(2, 0, "A2", True)
    state = state.ask(2, 1, "A1").answer(2, 1, "A1", True)
    state = state.ask(2, 1, "A3").answer(2, 1, "A3", True)

    assert projected_worlds(project_category_bitmap(state, 0, 2)) == {
        (0, 0, 0, 0)
    }

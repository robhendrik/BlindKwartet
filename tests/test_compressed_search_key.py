"""Diagnostics for the article-shaped global notebook key."""

from dataclasses import replace

from blind_kwartet.compressed_search_key import (
    compressed_projection,
    compressed_search_key,
    compressed_validation,
)
from blind_kwartet.search import SymmetryTransform, transform_state
from blind_kwartet.search_state import NO_OVERRIDE, SearchState


IDENTITY_CARDS = (tuple(range(4)),) * 3


def test_actor_normalization_is_cyclic_and_deterministic():
    keys = [compressed_search_key(SearchState.initial(actor=actor)) for actor in range(3)]
    assert keys[0] == keys[1] == keys[2]
    assert compressed_search_key(SearchState.initial()) == keys[0]


def test_reflection_does_not_collapse():
    state = replace(
        SearchState.initial(),
        current_owner_override=(1, NO_OVERRIDE, 2) + (NO_OVERRIDE,) * 9,
    )
    reflected = transform_state(
        state, SymmetryTransform((0, 2, 1), (0, 1, 2), IDENTITY_CARDS)
    )
    assert compressed_search_key(reflected) != compressed_search_key(state)


def test_unused_cards_and_equivalent_categories_collapse():
    state = SearchState.initial()
    card_swap = SymmetryTransform(
        (0, 1, 2), (0, 1, 2), ((1, 0, 2, 3), IDENTITY_CARDS[1], IDENTITY_CARDS[2])
    )
    category_swap = SymmetryTransform(
        (0, 1, 2), (1, 0, 2), IDENTITY_CARDS
    )
    assert compressed_search_key(transform_state(state, card_swap)) == compressed_search_key(state)
    named = replace(state, current_owner_override=(0,) + (NO_OVERRIDE,) * 11)
    assert compressed_search_key(transform_state(named, category_swap)) == compressed_search_key(named)


def test_public_transfer_is_retained_in_key():
    base = SearchState.initial()
    transferred = replace(base, current_owner_override=(1,) + base.T[1:])
    assert compressed_search_key(base) != compressed_search_key(transferred)


def test_different_authoritative_information_does_not_collide_in_basic_cases():
    base = SearchState.initial()
    no_a1 = base._filter(lambda deal_id: base.current_owner(deal_id, 0) != 1)
    yes_a1 = base._filter(lambda deal_id: base.current_owner(deal_id, 0) == 1)
    assert compressed_search_key(no_a1) != compressed_search_key(yes_a1)


def test_resolved_quartet_and_silence_relevant_information_is_present():
    base = SearchState.initial()
    forced = replace(base, current_owner_override=(0,) * 4 + (NO_OVERRIDE,) * 8)
    resolved_other_holder = replace(
        base, current_owner_override=(1,) * 4 + (NO_OVERRIDE,) * 8
    )
    assert compressed_search_key(forced) != compressed_search_key(resolved_other_holder)

    constrained = base._filter(lambda deal_id: base.current_owner(deal_id, 0) == 0)
    assert compressed_search_key(base) != compressed_search_key(constrained)


def test_projection_is_immutable_and_exposes_exact_world_count():
    state = SearchState.initial()
    projection = compressed_projection(state)
    assert projection["authoritative_worlds"] == state.D.bit_count()
    assert projection["key"] == compressed_search_key(state)
    assert isinstance(projection["key"].count_tables, tuple)
    validation = compressed_validation(state)
    assert validation["candidate_hall_consistent"]
    assert validation["transfer_markers_consistent"]
    assert validation["cross_category_world_correlations_encoded"] is False

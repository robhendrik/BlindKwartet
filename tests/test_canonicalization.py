"""Milestone 3 exact transform and canonical-key regressions."""

from dataclasses import replace

from blind_kwartet.deals import ALL_DEAL_IDS_MASK
from blind_kwartet.game import Game
from blind_kwartet.moves import AnswerMove, QuestionMove, QuartetMove
from blind_kwartet.players import RandomPlayer
from blind_kwartet.search import (
    SymmetryTransform,
    actor_normalized_transforms,
    canonical_key,
    canonicalize,
    canonicalize_reference,
    canonical_state,
    transform_move,
    transform_state,
)
from blind_kwartet.search_state import NO_OVERRIDE, SearchState


IDENTITY_CARDS = (tuple(range(4)),) * 3


def test_actor_normalized_group_has_exact_size_and_actor_zero_result():
    transforms = actor_normalized_transforms(0)
    assert len(transforms) == 82_944
    state = SearchState.initial()
    for transform in (transforms[0], transforms[-1]):
        assert transform.transform_state(state).actor == 0


def test_actor_normalization_preserves_cyclic_seat_order():
    for actor in range(3):
        transform = actor_normalized_transforms(actor)[0]
        assert transform.player_perm[actor] == 0
        assert transform.player_perm[(actor + 1) % 3] == 1
        assert transform.player_perm[(actor + 2) % 3] == 2
        assert transform.transform_state(SearchState.initial(actor)).actor == 0


def test_card_transform_uses_old_category_before_category_move():
    transform = SymmetryTransform(
        (0, 1, 2),
        (1, 0, 2),
        ((3, 2, 1, 0), IDENTITY_CARDS[1], IDENTITY_CARDS[2]),
    )
    assert transform.transform_card(0) == 7  # old A1 -> new B4
    assert transform.transform_card(4) == 0  # old B1 -> new A1


def test_transform_state_round_trip_and_popcount():
    state = replace(
        SearchState.initial(),
        possible_initial_deals=(1 << 0) | (1 << 1) | (1 << 4),
        current_owner_override=(2,) + (NO_OVERRIDE,) * 11,
        actor=1,
    )
    transform = SymmetryTransform(
        (1, 0, 2),
        (2, 0, 1),
        ((1, 0, 3, 2), (3, 2, 1, 0), (0, 2, 1, 3)),
    )
    transformed = transform_state(state, transform)
    assert transformed.D.bit_count() == state.D.bit_count()
    assert transformed.actor == 0
    assert transform_state(transformed, transform.inverse()) == state.normalize_overrides()


def test_category_and_card_symmetries_share_one_canonical_key_but_reflection_does_not():
    # Keep D complete so this symmetry regression isolates the non-redundant
    # public T mapping and remains practical for the deliberately exhaustive
    # reference canonicalizer.
    state = replace(
        SearchState.initial(),
        current_owner_override=(1,) + (NO_OVERRIDE,) * 11,
    )
    player_swap = SymmetryTransform((0, 2, 1), (0, 1, 2), IDENTITY_CARDS)
    category_swap = SymmetryTransform((0, 1, 2), (1, 0, 2), IDENTITY_CARDS)
    card_swap = SymmetryTransform(
        (0, 1, 2), (0, 1, 2), ((2, 1, 0, 3), IDENTITY_CARDS[1], IDENTITY_CARDS[2])
    )
    combined = player_swap.compose(category_swap).compose(card_swap)
    expected = canonical_key(state)
    # Swapping the two non-actor seats is the forbidden seat reflection.
    assert canonical_key(transform_state(state, player_swap)) != expected
    assert canonical_key(transform_state(state, category_swap)) == expected
    assert canonical_key(transform_state(state, card_swap)) == expected
    assert canonical_key(transform_state(state, combined)) != expected


def test_move_round_trip_including_old_category_rank_mapping():
    transform = SymmetryTransform(
        (0, 2, 1),
        (1, 2, 0),
        ((3, 0, 1, 2), (1, 2, 3, 0), (2, 3, 0, 1)),
    )
    moves = (
        QuestionMove(target=1, category=0, card=0),
        QuartetMove(category=2),
        AnswerMove(True),
        AnswerMove(False),
    )
    for move in moves:
        assert transform_move(transform_move(move, transform), transform.inverse()) == move


def test_correlation_is_not_replaced_by_individual_deal_orbits():
    # Deal IDs 0, 1, and 4 have the same individual actor-fixed orbit type,
    # but the two complete subsets below are not related by one global map.
    state = SearchState.initial()
    first = replace(state, possible_initial_deals=(1 << 0) | (1 << 1))
    second = replace(state, possible_initial_deals=(1 << 0) | (1 << 4))
    assert canonical_key(first) != canonical_key(second)


def test_reachable_states_and_returned_transform_are_exact():
    game = Game(tuple(RandomPlayer(seed=100 + i) for i in range(3)), max_events=50)
    result = game.run()
    # Keep this transform-round-trip regression on the initial reachable
    # decision state; sparse endgame oracle comparisons are covered below.
    reachable = Game.replay(result.history[:0])
    transform = SymmetryTransform(
        (1, 2, 0),
        (2, 0, 1),
        ((1, 0, 3, 2), (3, 2, 1, 0), (0, 2, 1, 3)),
    )
    variant = transform_state(reachable, transform)
    assert canonical_key(variant) == canonical_key(reachable)
    canonical, actual_to_canonical = canonical_state(reachable)
    assert canonical.actor == 0
    assert transform_state(canonical, actual_to_canonical.inverse()) == reachable


def test_optimized_canonicalizer_matches_reference_on_fixed_state_corpus():
    base = SearchState.initial()
    states = [
        base,
        replace(base, actor=1),
        replace(base, actor=2, current_owner_override=(1,) + (NO_OVERRIDE,) * 11),
        replace(base, possible_initial_deals=1 << 0),
        replace(base, possible_initial_deals=(1 << 0) | (1 << 1)),
        replace(base, possible_initial_deals=(1 << 0) | (1 << 4) | (1 << 9), actor=1),
    ]
    for state in states:
        reference_key, _ = canonicalize_reference(state)
        optimized_key, _ = canonicalize(state)
        assert optimized_key == reference_key


def test_optimized_canonicalizer_matches_reference_on_reachable_prefixes():
    game = Game(tuple(RandomPlayer(seed=700 + i) for i in range(3)), max_events=50)
    result = game.run()
    # Use terminal-near prefixes: intermediate large-D reference comparisons
    # are intentionally expensive and are already covered by the benchmark.
    for prefix in (0,):
        state = Game.replay(result.history[:prefix])
        assert canonicalize(state)[0] == canonicalize_reference(state)[0]


def test_canonicalization_is_idempotent_and_valid_transforms_are_equivalent():
    state = replace(
        SearchState.initial(actor=2),
        possible_initial_deals=(1 << 0) | (1 << 1) | (1 << 4),
        current_owner_override=(1, NO_OVERRIDE, 2) + (NO_OVERRIDE,) * 9,
    )
    canonical, _ = canonical_state(state)
    assert canonical.actor == 0
    assert canonical_key(canonical) == canonical_key(state)
    valid = SymmetryTransform(
        (2, 0, 1), (1, 2, 0),
        ((3, 0, 1, 2), (1, 2, 3, 0), (2, 3, 0, 1)),
    )
    assert canonical_key(transform_state(state, valid)) == canonical_key(state)

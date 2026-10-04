"""Milestone 1 exact-deal and SearchState regression tests."""

from dataclasses import replace

import pytest

from blind_kwartet.deals import INITIAL_DEALS, INITIAL_OWNER_MASKS
from blind_kwartet.referee import (
    Answer,
    Question,
    CARD_INDEX,
    generate_initial_worlds,
    information_state,
)
from blind_kwartet.search_state import NO_OVERRIDE, SearchState


def test_exact_initial_deal_universe_and_masks():
    assert len(INITIAL_DEALS) == 34_032
    assert sum(INITIAL_OWNER_MASKS[0][0] >> deal.deal_id & 1
               for deal in INITIAL_DEALS) == sum(
                   1 for deal in INITIAL_DEALS if deal.owner_by_card[0] == 0
               )


def test_initial_search_state_contains_all_deals():
    state = SearchState.initial()
    assert len(state.surviving_deal_ids()) == 34_032
    assert state.T == (NO_OVERRIDE,) * 12


def test_owner_lookup_uses_d_then_t():
    state = SearchState.initial()
    deal_id = state.surviving_deal_ids()[0]
    initial_owner = state.current_owner(deal_id, "A1")
    transferred = state.answer(0, initial_owner, "A1", True)
    assert transferred.current_owner(deal_id, "A1") == 0
    assert transferred.T[0] == NO_OVERRIDE


def test_yes_updates_t_and_no_does_not():
    state = SearchState.initial().ask(0, 1, "A1")
    yes = state.answer(0, 1, "A1", True)
    no = state.answer(0, 1, "A1", False)
    assert yes.T[0] == 0
    assert no.T == state.T


def test_eliminated_deals_never_return():
    state = SearchState.initial().ask(0, 1, "A1")
    after_no = state.answer(0, 1, "A1", False)
    after_yes = after_no.answer(2, 0, "A2", True)
    assert after_yes.D & ~after_no.D == 0
    assert after_no.D & ~state.D == 0


def test_card_can_be_transferred_back():
    # YES transfers A1 P2 -> P1.  A NO then passes the turn to P2, who asks
    # for A1 and receives it back.
    events = [
        Question(0, 1, "A1"), Answer(True),
        Question(0, 1, "A2"), Answer(False),
        Question(1, 0, "A1"), Answer(True),
    ]
    state = SearchState.initial().replay(events)
    # The second transfer returns A1 to its surviving initial owner, so the
    # public override is redundant and is normalized away.
    assert state.T[0] == NO_OVERRIDE
    assert state.actor == 1
    assert state.D


def test_cannot_ask_for_card_already_owned_by_asker():
    state = SearchState.initial()._filter(
        lambda deal_id: SearchState.initial().current_owner(deal_id, "A1") == 0
    )
    with pytest.raises(ValueError):
        state.ask(0, 1, "A1")


def test_yes_normalizes_override_implied_by_d():
    # Model a previous transfer: D says the initial owner is P1, while T
    # says the card currently belongs to P2.  A YES transfer back to P1 then
    # makes the override redundant.
    state = SearchState.initial()._filter(
        lambda deal_id: SearchState.initial().current_owner(deal_id, "A1") == 0
    )
    state = replace(state, current_owner_override=(1,) + state.T[1:])
    transferred = state.answer(0, 1, "A1", True)
    assert transferred.T[0] == NO_OVERRIDE


def test_scripted_replay_matches_reference_after_every_event():
    events = [
        Question(0, 1, "A1"), Answer(False),
        Question(1, 0, "A2"), Answer(True),
        Question(1, 0, "A1"), Answer(False),
    ]
    worlds = generate_initial_worlds()
    search = SearchState.initial()
    prefix = []
    actor = 0

    for event in events:
        prefix.append(event)
        # Replay from the complete public prefix because pending questions
        # are transient protocol context, not part of SearchState.
        search = SearchState.initial().replay(prefix)
        surviving_ids = information_state(list(worlds), prefix)
        old_initial = {
            worlds[index].owner_by_card for index in surviving_ids
        }
        new_initial = {
            INITIAL_DEALS[deal_id].owner_by_card
            for deal_id in search.surviving_deal_ids()
        }
        old_current = set()
        for index in surviving_ids:
            current = list(worlds[index].owner_by_card)
            pending = None
            for step in prefix:
                if isinstance(step, Question):
                    pending = step
                else:
                    if step.value:
                        current[CARD_INDEX[pending.card]] = pending.asker
                    pending = None
            old_current.add(tuple(current))
        new_current = {
            search.current_owners(deal_id)
            for deal_id in search.surviving_deal_ids()
        }
        assert len(surviving_ids) == len(search.surviving_deal_ids())
        assert old_initial == new_initial
        assert old_current == new_current

        if isinstance(event, Answer):
            actor = prefix[-2].asker if event.value else prefix[-2].target
        assert search.actor == actor

"""Tests for the brute-force Blind Kwartet referee."""

import pytest

from blind_kwartet.referee import (
    Question,
    Answer,
    generate_initial_worlds,
    information_state,
)


@pytest.fixture(scope="module")
def worlds():
    """Generate the reference set of legal initial worlds once."""
    return generate_initial_worlds(
        exclude_initial_quartets=True
    )


def state(worlds, events):
    """Convenience wrapper returning the information state."""
    return information_state(worlds, events)


# ---------------------------------------------------------------------------
# Basic reference tests
# ---------------------------------------------------------------------------

def test_number_of_initial_worlds(worlds):
    """There should be 34,032 legal initial worlds."""
    assert len(worlds) == 34_032


def test_empty_transcript_keeps_all_worlds(worlds):
    """Without observations, every initial world remains possible."""
    assert len(state(worlds, [])) == 34_032


# ---------------------------------------------------------------------------
# Contradictory answers
# ---------------------------------------------------------------------------

def test_same_player_cannot_answer_no_then_yes_without_transfer(worlds):
    """A card cannot suddenly appear at a player who just denied having it."""

    transcript = [
        Question(asker=0, target=1, card="A1"),
        Answer(False),

        # P3 now asks P2 exactly the same card.
        Question(asker=2, target=1, card="A1"),
        Answer(True),
    ]

    assert len(state(worlds, transcript)) == 0


def test_card_cannot_be_owned_by_two_players(worlds):
    """After a YES and transfer, the previous owner cannot still have the card."""

    transcript = [
        Question(asker=0, target=1, card="A1"),
        Answer(True),

        # A1 has moved from P2 to P1.
        # P3 asks P2 for it.
        Question(asker=2, target=1, card="A1"),
        Answer(True),
    ]

    assert len(state(worlds, transcript)) == 0


# ---------------------------------------------------------------------------
# Transfer logic
# ---------------------------------------------------------------------------

def test_yes_transfers_card_to_asker(worlds):
    """After YES, the asker must currently own the transferred card."""

    transcript = [
        Question(asker=0, target=1, card="A1"),
        Answer(True),

        # A1 must now be at P1.
        Question(asker=2, target=0, card="A1"),
        Answer(True),
    ]

    assert len(state(worlds, transcript)) > 0


def test_transferred_card_no_longer_at_previous_owner(worlds):
    """After transfer, the previous owner must answer NO."""

    transcript = [
        Question(asker=0, target=1, card="A1"),
        Answer(True),

        # P3 asks the old owner.
        Question(asker=2, target=1, card="A1"),
        Answer(False),
    ]

    assert len(state(worlds, transcript)) > 0


# ---------------------------------------------------------------------------
# Forced answers
# ---------------------------------------------------------------------------

def test_known_transferred_card_forces_yes(worlds):
    """Once a transfer is known, a contradictory NO must be impossible."""

    transcript = [
        Question(asker=0, target=1, card="A1"),
        Answer(True),

        # A1 is now definitely at P1.
        Question(asker=2, target=0, card="A1"),
        Answer(False),
    ]

    assert len(state(worlds, transcript)) == 0


# ---------------------------------------------------------------------------
# Information-state equivalence
# ---------------------------------------------------------------------------

def test_redundant_information_does_not_change_state(worlds):
    """A logically forced observation should not change the information state."""

    before = [
        Question(asker=0, target=1, card="A1"),
        Answer(True),

        # After this YES, A1 is known to be at P1.
        Question(asker=2, target=0, card="A1"),
    ]

    after = before + [
        Answer(True),
    ]

    state_before = state(worlds, before)
    state_after = state(worlds, after)

    assert state_before == state_after


# ---------------------------------------------------------------------------
# Questions themselves contain information
# ---------------------------------------------------------------------------

def test_question_can_reduce_possible_worlds(worlds):
    """Asking for family A reveals that the asker currently has an A card."""

    initial = state(worlds, [])

    after_question = state(
        worlds,
        [
            Question(
                asker=0,
                target=1,
                card="A1",
            )
        ],
    )

    assert len(after_question) < len(initial)


def test_redundant_question_does_not_reduce_worlds(worlds):
    """Once family ownership is known, another A question may add no information."""

    before = [
        Question(asker=0, target=1, card="A1"),
        Answer(False),
    ]

    after = before + [
        Question(asker=0, target=2, card="A2"),
    ]

    state_before = state(worlds, before)
    state_after = state(worlds, after)

    assert state_before == state_after
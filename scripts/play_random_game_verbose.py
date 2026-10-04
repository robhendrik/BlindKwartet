"""Run one reproducible random game with an information-state transcript.

The entropy printed here is ``log2(N)`` for a uniform prior over the
surviving legal initial-deal set.  It is entropy of the initial-deal
information state, not a complete measure of strategic uncertainty.
"""

from __future__ import annotations

from math import log2
import os

from blind_kwartet.deals import CARDS, ALL_DEAL_IDS_MASK
from blind_kwartet.game import Game
from blind_kwartet.history import AnswerEvent, QuartetEvent, QuestionEvent
from blind_kwartet.moves import AnswerMove, QuestionMove, QuartetMove
from blind_kwartet.players import RandomPlayer
from blind_kwartet.search_state import QuestionContext, SearchState


INITIAL_DEALS = ALL_DEAL_IDS_MASK.bit_count()


def entropy_bits(n_worlds: int) -> float:
    """Return ``log2(n_worlds)`` under the uniform surviving-world prior."""
    if n_worlds <= 0:
        raise ValueError("entropy is undefined for an empty information set")
    return log2(n_worlds)


def information_gain(n_before: int, n_after: int) -> float:
    """Return ``log2(n_before / n_after)`` for one public event."""
    if n_before <= 0 or n_after <= 0 or n_after > n_before:
        raise ValueError("world counts must be positive and non-increasing")
    return log2(n_before / n_after)


def _player(player: int) -> str:
    return f"P{player + 1}"


def _card(card: int) -> str:
    return CARDS[card]


def _world_line(n_worlds: int) -> str:
    return (
        f"possible deals: {n_worlds}; entropy: {entropy_bits(n_worlds):.6f} bits; "
        f"universe remaining: {100 * n_worlds / INITIAL_DEALS:.4f}%"
    )


def _transition_line(n_before: int, n_after: int) -> str:
    return (
        f"possible deals: {n_after}; entropy: {entropy_bits(n_after):.6f} bits; "
        f"universe remaining: {100 * n_after / INITIAL_DEALS:.4f}%; "
        f"information gained: {information_gain(n_before, n_after):.6f} bits"
    )


def _forced_resolutions(
    before: SearchState, after: SearchState, *, exclude: set[int] | None = None
) -> tuple[tuple[int, int], ...]:
    excluded = exclude or set()
    categories = after.resolved_categories - before.resolved_categories
    return tuple(
        (category, after.quartet_holders()[category])
        for category in sorted(categories)
        if category not in excluded
    )


def print_transcript(result) -> None:
    """Print the structured history while replaying exact state transitions."""
    state = SearchState.initial()
    pending: QuestionContext | None = None
    question_count = yes_count = no_count = forced_answer_count = 0
    voluntary_quartets = forced_quartets = 0

    print("Blind Kwartet verbose random game")
    print("seeds: P1=100, P2=101, P3=102; game seed=123")
    print("initial", _world_line(state.D.bit_count()))

    for event_number, event in enumerate(result.history, start=1):
        if isinstance(event, QuestionEvent):
            question_count += 1
            move = QuestionMove(event.target, event.category, event.card)
            before = state
            pending = state.apply_question(move)
            after_question = pending.state
            print(f"\n[event {event_number}] {_player(event.asker)} asks "
                  f"{_player(event.target)} for {_card(event.card)}")
            print("  before:", _world_line(before.D.bit_count()))
            print("  after asking:", _transition_line(
                before.D.bit_count(), after_question.D.bit_count()))
            print(f"  answerer: {_player(event.target)}; next actor: "
                  f"{_player(event.target)} (answer pending)")
            continue

        if isinstance(event, AnswerEvent):
            if pending is None:
                raise AssertionError("answer without pending question")
            before = pending.state
            legal_answers = pending.legal_answers()
            forced = len(legal_answers) == 1
            forced_answer_count += int(forced)
            answer = AnswerMove(event.yes)
            after = pending.apply_answer(answer)
            if event.yes:
                yes_count += 1
                label = "YES"
            else:
                no_count += 1
                label = "NO"
            print(f"\n[event {event_number}] {_player(event.target)} answers {label}"
                  f" ({'forced' if forced else 'strategic'})")
            print("  before answer:", _world_line(before.D.bit_count()))
            print("  after answer:", _transition_line(
                before.D.bit_count(), after.D.bit_count()))
            if event.yes:
                print(f"  transfer: {_card(event.card)} "
                      f"{_player(event.target)} -> {_player(event.asker)}")
            resolutions = _forced_resolutions(before, after)
            for category, holder in resolutions:
                forced_quartets += 1
                print(f"  forced quartet: {chr(ord('A') + category)} by {_player(holder)}")
            print(f"  next actor: {_player(after.actor)}")
            state = after
            pending = None
            continue

        if isinstance(event, QuartetEvent):
            before = state
            # QuartetEvent stores the canonical category directly.
            after = state.apply_quartet(QuartetMove(event.category))
            voluntary_quartets += 1
            resolutions = _forced_resolutions(before, after, exclude={event.category})
            print(f"\n[event {event_number}] {_player(event.player)} declares "
                  f"quartet {chr(ord('A') + event.category)} (voluntary)")
            print("  before:", _world_line(before.D.bit_count()))
            print("  after declaration:", _transition_line(
                before.D.bit_count(), after.D.bit_count()))
            for category, holder in resolutions:
                forced_quartets += 1
                print(f"  forced quartet: {chr(ord('A') + category)} by {_player(holder)}")
            print(f"  next actor: {_player(after.actor)}")
            state = after
            continue

        raise TypeError(f"unknown event: {event!r}")

    initial_entropy = entropy_bits(INITIAL_DEALS)
    final_deals = result.final_state.D.bit_count()
    final_entropy = entropy_bits(final_deals)
    total_gain = information_gain(INITIAL_DEALS, final_deals)
    winners = ", ".join(_player(seat) for seat in result.winner_seats) or "none"
    print("\nSummary")
    print(f"final quartet scores: {result.seat_scores}")
    print(f"winner(s): {winners}")
    print(f"end reason: {result.end_reason}")
    print(f"total events: {result.n_events}")
    print(f"questions: {question_count}; YES: {yes_count}; NO: {no_count}")
    print(f"forced answers: {forced_answer_count}")
    print(f"voluntary quartets: {voluntary_quartets}; forced quartets: {forced_quartets}")
    print(f"initial possible deals: {INITIAL_DEALS}")
    print(f"final possible deals: {final_deals}")
    print(f"initial entropy: {initial_entropy:.6f} bits")
    print(f"final entropy: {final_entropy:.6f} bits")
    print(f"total information gained: {total_gain:.6f} bits")


def main() -> None:
    players = tuple(RandomPlayer(seed=100 + seat) for seat in range(3))
    result = Game(players, seed=123, max_events=300).run()
    print_transcript(result)


if __name__ == "__main__":
    main()

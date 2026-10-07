"""Measure complete-game behavior of SingleCategoryTreePlayer.

This is a deterministic diagnostic, not a tournament or a strategy change.
Run from the repository root, for example::

    PYTHONPATH=src:. python -u scripts/benchmark_single_category_tree.py \
        --games 10 --seed 123
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from statistics import mean
from typing import Iterable

from blind_kwartet.game import Game
from blind_kwartet.history import AnswerEvent, QuartetEvent, QuestionEvent
from blind_kwartet.moves import AnswerMove, QuestionMove, QuartetMove
from blind_kwartet.players import (
    RandomPlayer,
    SingleCategoryTreePlayer,
    TreeDecisionDiagnostic,
)
from blind_kwartet.result import GameResult
from blind_kwartet.single_category_solver import CategoryOutcome
from blind_kwartet.search_state import SearchState


@dataclass(frozen=True)
class GameObservation:
    tree_seat: int | None
    scores: tuple[int, ...]
    winners: tuple[int, ...]
    tree_score: int | None
    events: int
    end_reason: str
    decision_diagnostics: tuple[TreeDecisionDiagnostic, ...]

    @property
    def event_limit_reached(self) -> bool:
        return self.end_reason == "event_limit"


@dataclass(frozen=True)
class AllTreeObservation:
    """Diagnostics for one complete (or event-limited) all-tree game."""

    result: GameResult
    players: tuple[SingleCategoryTreePlayer, ...]
    question_decisions: tuple[int, ...]
    strategic_answer_decisions: tuple[int, ...]
    selected_outcomes: tuple[Counter, ...]
    first_win_event: tuple[int | None, ...]
    category_switches: tuple[int, ...]
    repeated_search_states: int
    distinct_search_states: int
    final_deal_count: int
    first_singleton_event: int | None

    @property
    def event_limit_reached(self) -> bool:
        return self.result.end_reason == "event_limit"


def run_all_tree_game(*, seed: int = 123, event_limit: int = 500) -> AllTreeObservation:
    """Run one game with three identical deterministic tree strategies."""
    players = tuple(SingleCategoryTreePlayer() for _ in range(3))
    result = Game(players, first_player=0, seed=seed, max_events=event_limit).run()

    # Replay the public history to inspect the exact strategic states.  The
    # transient state between QuestionEvent and AnswerEvent is intentionally
    # not counted: it is not a SearchState in the game model.
    state = SearchState.initial(0).resolve_forced_quartets()
    states = [state]
    pending = None
    pending_has_strategic_answer = False
    question_decisions = [0, 0, 0]
    strategic_answers = [0, 0, 0]
    outcomes = [Counter() for _ in range(3)]
    first_win = [None, None, None]
    switches = [0, 0, 0]
    last_category = [None, None, None]
    diagnostic_indices = [0, 0, 0]

    for event_number, event in enumerate(result.history, start=1):
        if isinstance(event, QuestionEvent):
            pending = state.apply_question(QuestionMove(event.target, event.category, event.card))
            seat = event.asker
            diagnostic = players[seat].decision_diagnostics[diagnostic_indices[seat]]
            diagnostic_indices[seat] += 1
            question_decisions[seat] += 1
            assert diagnostic.action_kind == "question"
            label = diagnostic.selected_outcome.name
            outcomes[seat][label] += 1
            if diagnostic.evaluated_win and first_win[seat] is None:
                first_win[seat] = event_number
            if last_category[seat] is not None and last_category[seat] != event.category:
                switches[seat] += 1
            last_category[seat] = event.category
            pending_has_strategic_answer = len(pending.legal_answers()) == 2
            if pending_has_strategic_answer:
                strategic_answers[event.target] += 1
        elif isinstance(event, AnswerEvent):
            assert pending is not None
            state = pending.apply_answer(AnswerMove(event.yes))
            if pending_has_strategic_answer:
                seat = event.target
                diagnostic = players[seat].decision_diagnostics[diagnostic_indices[seat]]
                diagnostic_indices[seat] += 1
                assert diagnostic.action_kind == "answer"
            pending = None
            pending_has_strategic_answer = False
            states.append(state)
        elif isinstance(event, QuartetEvent):
            state = state.apply_quartet(QuartetMove(event.category))
            seat = event.player
            diagnostic = players[seat].decision_diagnostics[diagnostic_indices[seat]]
            diagnostic_indices[seat] += 1
            assert diagnostic.action_kind == "quartet"
            states.append(state)
        else:
            raise TypeError(event)

    counts = Counter(states)
    repeated = sum(count - 1 for count in counts.values() if count > 1)
    singleton_event = next(
        (index for index, item in enumerate(states[1:], start=1) if item.D.bit_count() == 1),
        None,
    )
    return AllTreeObservation(
        result=result,
        players=players,
        question_decisions=tuple(question_decisions),
        strategic_answer_decisions=tuple(strategic_answers),
        selected_outcomes=tuple(outcomes),
        first_win_event=tuple(first_win),
        category_switches=tuple(switches),
        repeated_search_states=repeated,
        distinct_search_states=len(counts),
        final_deal_count=state.D.bit_count(),
        first_singleton_event=singleton_event,
    )


def observe_game(
    result: GameResult,
    *,
    tree_seat: int | None,
    diagnostics: Iterable[TreeDecisionDiagnostic] = (),
) -> GameObservation:
    return GameObservation(
        tree_seat=tree_seat,
        scores=result.seat_scores,
        winners=result.winner_seats,
        tree_score=None if tree_seat is None else result.seat_scores[tree_seat],
        events=result.n_events,
        end_reason=result.end_reason,
        decision_diagnostics=tuple(diagnostics),
    )


def run_tree_game(tree_seat: int, game_number: int, seed: int, event_limit: int) -> GameObservation:
    game_seed = seed + game_number * 1_009 + tree_seat * 100_003
    tree = SingleCategoryTreePlayer()
    players = tuple(
        tree if seat == tree_seat else RandomPlayer(seed=game_seed + 17 * seat + 1)
        for seat in range(3)
    )
    result = Game(
        players,
        first_player=0,
        seed=game_seed,
        max_events=event_limit,
    ).run()
    return observe_game(
        result,
        tree_seat=tree_seat,
        diagnostics=tree.decision_diagnostics,
    )


def run_random_game(game_number: int, seed: int, event_limit: int) -> GameObservation:
    game_seed = seed + game_number * 1_009 + 700_000
    players = tuple(RandomPlayer(seed=game_seed + 17 * seat + 1) for seat in range(3))
    result = Game(
        players,
        first_player=0,
        seed=game_seed,
        max_events=event_limit,
    ).run()
    return observe_game(result, tree_seat=None)


def classify_game(observation: GameObservation) -> str:
    """Classify a tree seat's result, treating event limits as non-wins."""
    if observation.tree_seat is not None and observation.winners == (observation.tree_seat,):
        return "win"
    if observation.tree_seat is not None and observation.tree_seat in observation.winners:
        return "tie"
    return "loss"


def classify_decision(diagnostic: TreeDecisionDiagnostic) -> str:
    if diagnostic.action_kind != "question":
        raise ValueError("decision situation requires a question diagnostic")
    if diagnostic.evaluated_win:
        return "at least one WIN"
    if diagnostic.evaluated_open:
        return "no WIN but at least one OPEN"
    return "LOSS only"


def best_value_pairs(diagnostic: TreeDecisionDiagnostic) -> set[str]:
    values = {value for _, value in diagnostic.category_best_values}
    pairs = set()
    if CategoryOutcome.WIN in values and CategoryOutcome.OPEN in values:
        pairs.add("one category WIN, another OPEN")
    if CategoryOutcome.WIN in values and CategoryOutcome.LOSS in values:
        pairs.add("one category WIN, another LOSS")
    if CategoryOutcome.OPEN in values and CategoryOutcome.LOSS in values:
        pairs.add("one category OPEN, another LOSS")
    return pairs


def _pct(part: int, total: int) -> str:
    return f"{100.0 * part / total:6.2f}%" if total else "  0.00%"


def _tree_table(observations: list[GameObservation]) -> None:
    print("\nGame performance versus RandomPlayer")
    print("seat   games   wins   ties   losses   win_rate   mean_score   mean_events")
    for seat in range(3):
        games = [observation for observation in observations if observation.tree_seat == seat]
        counts = Counter(classify_game(observation) for observation in games)
        print(
            f"P{seat + 1:<4} {len(games):5d} {counts['win']:6d} {counts['tie']:6d} "
            f"{counts['loss']:7d} {_pct(counts['win'], len(games)):>9} "
            f"{mean(observation.tree_score for observation in games):11.2f} "
            f"{mean(observation.events for observation in games):12.2f}"
        )


def _random_summary(observations: list[GameObservation]) -> None:
    event_limits = sum(observation.event_limit_reached for observation in observations)
    winner_counts = Counter(
        seat for observation in observations for seat in observation.winners
    )
    ties = sum(len(observation.winners) > 1 for observation in observations)
    print("\nAll-Random baseline")
    print(f"games={len(observations)} event_limits={event_limits} ties={ties}")
    print(
        "winner seats: "
        + ", ".join(f"P{seat + 1}={winner_counts[seat]}" for seat in range(3))
    )
    print(f"mean_events={mean(observation.events for observation in observations):.2f}")


def _decision_summary(observations: list[GameObservation]) -> None:
    decisions = [
        diagnostic
        for observation in observations
        for diagnostic in observation.decision_diagnostics
        if diagnostic.action_kind == "question"
    ]
    situations = Counter(classify_decision(diagnostic) for diagnostic in decisions)
    print("\nDecision summary")
    print("situation                                      count   percent")
    for label in ("at least one WIN", "no WIN but at least one OPEN", "LOSS only"):
        print(f"{label:<45} {situations[label]:5d} {_pct(situations[label], len(decisions)):>8}")

    loss_only = [diagnostic for diagnostic in decisions if classify_decision(diagnostic) == "LOSS only"]
    loss_by_unresolved = Counter(diagnostic.unresolved_categories for diagnostic in loss_only)
    print("\nLOSS-only decisions by unresolved categories")
    for unresolved in (1, 2, 3):
        count = loss_by_unresolved[unresolved]
        print(f"unresolved categories = {unresolved}: {count:5d} {_pct(count, len(loss_only)):>8}")

    cross = Counter()
    for diagnostic in decisions:
        values = {value for _, value in diagnostic.category_best_values}
        if len(values) <= 1:
            cross["all categories same value"] += 1
        else:
            cross.update(best_value_pairs(diagnostic))
            if len(values) == 3:
                cross["all three values present"] += 1
    print("\nCross-category best-local-value diagnostics")
    print("situation                                      count   percent")
    labels = (
        "one category WIN, another OPEN",
        "one category WIN, another LOSS",
        "one category OPEN, another LOSS",
        "all three values present",
        "all categories same value",
    )
    for label in labels:
        print(f"{label:<45} {cross[label]:5d} {_pct(cross[label], len(decisions)):>8}")

    collapsed = sum(diagnostic.deals_collapsed for diagnostic in decisions)
    deal_counts = [diagnostic.possible_initial_deals for diagnostic in decisions]
    unresolved_mean = mean(diagnostic.unresolved_categories for diagnostic in decisions) if decisions else 0.0
    print("\nDecision-state diagnostics")
    print(f"|D| == 1: {_pct(collapsed, len(decisions))}")
    if deal_counts:
        print(f"|D| min/mean/max: {min(deal_counts)} / {mean(deal_counts):.2f} / {max(deal_counts)}")
    else:
        print("|D| min/mean/max: 0 / 0.00 / 0")
    print(f"mean unresolved categories: {unresolved_mean:.2f}")
    print(
        "solver totals: "
        f"nodes={sum(diagnostic.solver_nodes for diagnostic in decisions)} "
        f"memo_hits={sum(diagnostic.solver_memo_hits for diagnostic in decisions)} "
        f"cycle_hits={sum(diagnostic.solver_cycle_hits for diagnostic in decisions)}"
    )
    print(f"tree games hitting event_limit: {sum(observation.event_limit_reached for observation in observations)}")


def run_benchmark(games: int, seed: int, event_limit: int) -> None:
    tree_observations = [
        run_tree_game(seat, game, seed, event_limit)
        for seat in range(3)
        for game in range(games)
    ]
    random_observations = [
        run_random_game(game, seed, event_limit) for game in range(games)
    ]
    _tree_table(tree_observations)
    _random_summary(random_observations)
    _decision_summary(tree_observations)


def _event_text(event: object) -> str:
    if isinstance(event, QuestionEvent):
        return f"QUESTION P{event.asker + 1}->P{event.target + 1} C{event.category + 1} card={event.card}"
    if isinstance(event, AnswerEvent):
        return f"ANSWER P{event.target + 1} {'YES' if event.yes else 'NO'} C{event.category + 1} card={event.card}"
    if isinstance(event, QuartetEvent):
        return f"QUARTET P{event.player + 1} C{event.category + 1}"
    return repr(event)


def print_all_tree_observation(observation: AllTreeObservation, *, verbose: bool = False) -> None:
    result = observation.result
    print("All-tree game")
    print(f"scores={result.seat_scores} winners={tuple(seat + 1 for seat in result.winner_seats)}")
    print(f"events={result.n_events} end_reason={result.end_reason} event_limit_hit={observation.event_limit_reached}")
    for seat, player in enumerate(observation.players):
        outcomes = observation.selected_outcomes[seat]
        print(
            f"P{seat + 1}: questions={observation.question_decisions[seat]} "
            f"strategic_answers={observation.strategic_answer_decisions[seat]} "
            f"WIN={outcomes['WIN']} OPEN={outcomes['OPEN']} LOSS={outcomes['LOSS']} "
            f"first_WIN_event={observation.first_win_event[seat]} "
            f"category_switches={observation.category_switches[seat]} "
            f"solver_nodes={player.solver_nodes} memo_hits={player.solver_memo_hits} "
            f"cycle_hits={player.solver_cycle_hits}"
        )
    print(
        f"repeated_exact_SearchStates={observation.repeated_search_states} "
        f"distinct_SearchStates={observation.distinct_search_states} "
        f"final_|D|={observation.final_deal_count} "
        f"first_|D|=1_event={observation.first_singleton_event}"
    )
    if verbose:
        print("Transcript")
        for event_number, event in enumerate(result.history, start=1):
            print(f"{event_number:3d}: {_event_text(event)}")


def run_all_tree(*, seed: int, event_limit: int, repeat: int, verbose: bool) -> None:
    observations = [
        run_all_tree_game(seed=seed, event_limit=event_limit)
        for _ in range(repeat)
    ]
    for index, observation in enumerate(observations, start=1):
        print(f"\nRun {index}/{repeat}")
        print_all_tree_observation(observation, verbose=verbose)
    trajectories = [
        (observation.result.seat_scores, observation.result.winner_seats,
         observation.result.end_reason, observation.result.history)
        for observation in observations
    ]
    print(f"repeated_runs_identical={len(set(trajectories)) == 1}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--games", type=int, default=100)
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--event-limit", type=int, default=500)
    parser.add_argument("--all-tree", action="store_true", help="run three identical tree players")
    parser.add_argument("--repeat", type=int, default=3, help="repeat the identical all-tree setup")
    parser.add_argument("--verbose", action="store_true", help="print the full all-tree transcript")
    args = parser.parse_args()
    if args.games <= 0 or args.event_limit < 0 or args.repeat <= 0:
        parser.error("--games/--repeat must be positive and --event-limit must be non-negative")
    if args.all_tree:
        run_all_tree(seed=args.seed, event_limit=args.event_limit, repeat=args.repeat, verbose=args.verbose)
    else:
        run_benchmark(args.games, args.seed, args.event_limit)


if __name__ == "__main__":
    main()

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
from blind_kwartet.players import (
    RandomPlayer,
    SingleCategoryTreePlayer,
    TreeDecisionDiagnostic,
)
from blind_kwartet.result import GameResult
from blind_kwartet.single_category_solver import CategoryOutcome


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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--games", type=int, default=100)
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--event-limit", type=int, default=500)
    args = parser.parse_args()
    if args.games <= 0 or args.event_limit < 0:
        parser.error("--games must be positive and --event-limit must be non-negative")
    run_benchmark(args.games, args.seed, args.event_limit)


if __name__ == "__main__":
    main()

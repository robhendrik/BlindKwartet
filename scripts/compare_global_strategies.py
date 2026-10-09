"""Compare local and global Blind Kwartet decisions on deterministic games.

Examples::

    PYTHONPATH=src:. python scripts/compare_global_strategies.py \
        --mode both --driver local --depths 1,2,3 --repeat 1 \
        --event-limit 50 --output results/compare.jsonl \
        --summary results/compare.md

The script deliberately delegates all legality, answers, transfers, and
terminal handling to ``Game`` and ``SearchState``.  It only observes each
PlayerView, evaluates policies on that immutable view, and returns the
configured driver's move.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import sys
import time
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from blind_kwartet.game import Game
from blind_kwartet.history import AnswerEvent, GameEvent, QuestionEvent, QuartetEvent
from blind_kwartet.moves import AnswerMove, Move, QuestionMove, QuartetMove
from blind_kwartet.players import (
    Player,
    PlayerView,
    SingleCategoryTreePlayer,
    _GlobalSearch,
    semantic_question_representatives,
)
from blind_kwartet.result import GameResult
from blind_kwartet.search_state import SearchState
from blind_kwartet.single_category_solver import CategoryOutcome, SingleCategorySolver


def _json_value(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_json_value(item) for item in value]
    if isinstance(value, CategoryOutcome):
        return value.name
    if isinstance(value, (QuestionMove, AnswerMove, QuartetMove)):
        return format_move(value)
    return value


def format_move(move: Move | None) -> str | None:
    """Return a stable human-readable labelled move."""
    if move is None:
        return None
    if isinstance(move, QuestionMove):
        category = chr(ord("A") + move.category)
        card = move.card % 4 + 1
        return f"P{move.target + 1} {category}{card}"
    if isinstance(move, QuartetMove):
        return f"quartet {chr(ord('A') + move.category)}"
    if isinstance(move, AnswerMove):
        return "YES" if move.yes else "NO"
    raise TypeError(f"unsupported move: {move!r}")


def _question_equivalent(state: SearchState, first: Move, second: Move) -> bool:
    if not isinstance(first, QuestionMove) or not isinstance(second, QuestionMove):
        return first == second
    return len(semantic_question_representatives(state, (first, second))) == 1


def semantically_equal(state: SearchState, first: Move | None, second: Move | None) -> bool:
    if first is None or second is None:
        return first is second
    return _question_equivalent(state, first, second)


def display_move(state: SearchState, move: Move | None, peers: Iterable[Move | None] = ()) -> str | None:
    """Display equivalent question labels using one local representative."""
    if move is None:
        return None
    if isinstance(move, QuestionMove):
        for peer in peers:
            if isinstance(peer, QuestionMove) and _question_equivalent(state, move, peer):
                move = min((move, peer), key=lambda item: (item.category, item.card, item.target))
        return f"P{move.target + 1} asks {chr(ord('A') + move.category)}{move.card % 4 + 1}"
    return format_move(move)


def _local_value(player: SingleCategoryTreePlayer, move: Move) -> Any:
    diagnostic = player.decision_diagnostics[-1] if player.decision_diagnostics else None
    if isinstance(move, AnswerMove):
        return None if diagnostic is None else diagnostic.selected_answer
    if isinstance(move, QuartetMove):
        return {"kind": "quartet", "category": move.category}
    if diagnostic is None:
        return None
    return None if diagnostic.selected_outcome is None else diagnostic.selected_outcome.name


@dataclass
class PolicyResult:
    move: Move
    value: Any
    diagnostics: dict[str, Any]
    candidates: list[dict[str, Any]]


def _global_result(view: PlayerView, depth: int) -> PolicyResult:
    started = time.perf_counter()
    search = _GlobalSearch(SingleCategorySolver())
    if any(isinstance(action, AnswerMove) for action in view.legal_actions):
        question_event = next(
            event for event in reversed(view.history) if isinstance(event, QuestionEvent)
        )
        question = QuestionMove(
            question_event.target, question_event.category, question_event.card
        )
        context = view.state.apply_question(question)
        choice, yes_value, no_value = search.evaluate_answer_branches(
            context, view.player_id, depth - 1
        )
        candidate_values = {
            "YES": _json_value(yes_value),
            "NO": _json_value(no_value),
        }
        value = yes_value if choice.yes else no_value
        candidates = [
            {"move": "YES", "value": _json_value(yes_value)},
            {"move": "NO", "value": _json_value(no_value)},
        ]
    else:
        actions = search.search_actions(view.state, view.legal_actions, depth)
        evaluated = [(action, search.evaluate_action(view.state, action, depth)) for action in actions]
        selected = max(range(len(evaluated)), key=lambda index: evaluated[index][1][view.player_id])
        choice, value = evaluated[selected]
        candidate_values = {format_move(action): _json_value(item) for action, item in evaluated}
        candidates = [
            {"move": format_move(action), "value": _json_value(item)}
            for action, item in evaluated
        ]
    elapsed_ms = (time.perf_counter() - started) * 1000
    diagnostics = {
        "depth": depth,
        "selected_move": format_move(choice),
        "returned_value": _json_value(value),
        "nodes_expanded": search.nodes_expanded,
        "raw_legal_questions": search.raw_legal_questions,
        "semantic_question_classes": search.semantic_question_classes,
        "pruned_questions": search.pruned_equivalent_questions,
        "leaf_evaluations": search.leaf_evaluations,
        "runtime_ms": elapsed_ms,
        "branching_by_depth": search.symmetry_diagnostics["by_depth"],
        "candidate_values": candidate_values,
    }
    return PolicyResult(choice, _json_value(value), diagnostics, candidates)


class ComparisonPlayer(Player):
    """Evaluate every configured policy and return only the driver move."""

    def __init__(self, driver: str, depths: tuple[int, ...], records: list[dict[str, Any]]) -> None:
        self.driver = driver
        self.depths = depths
        self.records = records
        self.local_player = SingleCategoryTreePlayer(global_depth=0)

    def play(self, view: PlayerView) -> Move:
        before = view.state
        local_move = self.local_player.play(view)
        local_result = PolicyResult(
            local_move,
            _local_value(self.local_player, local_move),
            {"depth": 0, "selected_move": format_move(local_move)},
            [],
        )
        global_results = {depth: _global_result(view, depth) for depth in self.depths}
        all_moves = [local_move, *(result.move for result in global_results.values())]
        deviations = {
            "local_vs_depth": {
                str(depth): not semantically_equal(before, local_move, result.move)
                for depth, result in global_results.items()
            },
            "depth_vs_next": {
                f"{left}_vs_{right}": not semantically_equal(
                    before, global_results[left].move, global_results[right].move
                )
                for left, right in zip(self.depths, self.depths[1:])
            },
        }
        record = {
            "event_index": len(view.history),
            "actor": view.player_id,
            "possible_deals": before.D.bit_count(),
            "compact_t": "".join("-" if owner < 0 else str(owner) for owner in before.T),
            "unresolved_categories": 3 - len(before.resolved_categories),
            "driver_strategy": self.driver,
            "local": {
                "move": display_move(before, local_move, all_moves),
                "value": _json_value(local_result.value),
                "candidates": local_result.candidates,
            },
            "global": {
                str(depth): {
                    **result.diagnostics,
                    "move": display_move(before, result.move, all_moves),
                    "candidates": [
                        {
                            **candidate,
                            "move": display_move(before, result.move, all_moves)
                            if candidate["move"] == format_move(result.move)
                            else candidate["move"],
                        }
                        for candidate in result.candidates
                    ],
                }
                for depth, result in global_results.items()
            },
            "deviations": deviations,
        }
        self.records.append(record)
        if self.driver == "local":
            chosen = local_move
        else:
            chosen = global_results[int(self.driver)].move
        # The policy evaluations above are pure observations.  Assert that the
        # state object supplied by Game was not replaced or mutated.
        assert view.state is before
        return chosen


def _driver_value(driver: str) -> str:
    return "local" if driver == "local" else str(int(driver))


def run_game(*, driver: str, depths: tuple[int, ...], seed: int, event_limit: int) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    players = tuple(ComparisonPlayer(driver, depths, records) for _ in range(3))
    result = Game(players, first_player=0, seed=seed, max_events=event_limit).run()
    return {
        "seed": seed,
        "driver": driver,
        "depths": list(depths),
        "event_limit": event_limit,
        "result": {
            "scores": list(result.seat_scores),
            "winners": list(result.winner_seats),
            "events": result.n_events,
            "end_reason": result.end_reason,
        },
        "decisions": records,
    }


def _deviation_count(games: list[dict[str, Any]], left: str, right: str) -> int:
    count = 0
    for game in games:
        for decision in game["decisions"]:
            if left == "local":
                if decision["deviations"]["local_vs_depth"].get(right) is True:
                    count += 1
            elif decision["deviations"]["depth_vs_next"].get(f"{left}_vs_{right}") is True:
                count += 1
    return count


def write_summary(path: Path, games: list[dict[str, Any]], depths: tuple[int, ...]) -> None:
    completed = len(games)
    decisions = sum(len(game["decisions"]) for game in games)
    events = [game["result"]["events"] for game in games]
    lines = [
        "# Strategy comparison summary",
        "",
        f"games completed: {completed}",
        f"decisions inspected: {decisions}",
        f"mean events: {(sum(events) / len(events)) if events else 0:.2f}",
        "",
        "## Outcomes",
        "",
    ]
    for index, game in enumerate(games):
        result = game["result"]
        lines.append(
            f"- game {index}: driver={game['driver']} seed={game['seed']} "
            f"scores={tuple(result['scores'])} winners={tuple(result['winners'])} "
            f"events={result['events']} end={result['end_reason']}"
        )
    lines += ["", "## Deviations", ""]
    for depth in depths:
        lines.append(f"local vs depth {depth}: {_deviation_count(games, 'local', str(depth))}")
    for left, right in zip(depths, depths[1:]):
        lines.append(f"depth {left} vs depth {right}: {_deviation_count(games, str(left), str(right))}")
    lines += ["", "Chronological deviations:", ""]
    for game_index, game in enumerate(games):
        for decision in game["decisions"]:
            flags = [
                f"local-vs-{depth}"
                for depth, different in decision["deviations"]["local_vs_depth"].items()
                if different
            ] + [
                f"depth-{pair}"
                for pair, different in decision["deviations"]["depth_vs_next"].items()
                if different
            ]
            if flags:
                lines.append(
                    f"- game {game_index}, event {decision['event_index']}, "
                    f"actor P{decision['actor'] + 1}, |D|={decision['possible_deals']}: "
                    + ", ".join(flags)
                )
                lines.append(f"  local: {decision['local']['move']} value={decision['local']['value']}")
                for depth in depths:
                    item = decision["global"][str(depth)]
                    lines.append(f"  depth {depth}: {item['move']} value={item['returned_value']}")
                lines.append(f"  driver: {decision['driver_strategy']}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _load_games(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("decision", "games", "both"), default="decision")
    parser.add_argument("--depths", default="1,2,3")
    parser.add_argument("--driver", choices=("local", "1", "2", "3"), default="local")
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--event-limit", type=int, default=500)
    parser.add_argument("--output", type=Path, default=Path("results/strategy_compare.jsonl"))
    parser.add_argument("--summary", type=Path, default=Path("results/strategy_compare.md"))
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args(argv)
    depths = tuple(sorted({int(item) for item in args.depths.split(",") if item.strip()}))
    if not depths or any(depth < 1 for depth in depths):
        parser.error("--depths must contain positive integers")
    if args.repeat < 1 or args.event_limit < 0:
        parser.error("--repeat must be positive and --event-limit must be non-negative")
    if args.driver != "local" and int(args.driver) not in depths:
        parser.error("the numeric --driver must be included in --depths")

    plan: list[tuple[str, str, int]] = []
    if args.mode in {"decision", "both"}:
        plan.extend(("decision", args.driver, index) for index in range(args.repeat))
    if args.mode in {"games", "both"}:
        plan.extend(
            ("games", driver, index)
            for driver in ["local", *(str(depth) for depth in depths)]
            for index in range(args.repeat)
        )
    games = _load_games(args.output) if args.resume else []
    completed = {
        (game.get("driver"), game.get("game_index"), game.get("run_mode"))
        for game in games
    }
    if not args.resume and args.output.exists():
        args.output.unlink()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("a", encoding="utf-8") as stream:
        for run_mode, driver, index in plan:
            if args.resume and (driver, index, run_mode) in completed:
                continue
            game = run_game(
                driver=driver,
                depths=depths,
                seed=args.seed + index,
                event_limit=args.event_limit,
            )
            game["game_index"] = index
            game["run_mode"] = run_mode
            stream.write(json.dumps(game, sort_keys=True) + "\n")
            stream.flush()
            games.append(game)
            print(
                f"{run_mode}/{driver} game {index + 1}/{args.repeat}: scores={tuple(game['result']['scores'])} "
                f"events={game['result']['events']} end={game['result']['end_reason']}",
                flush=True,
            )
    if args.mode in {"decision", "both", "games"}:
        write_summary(args.summary, games, depths)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

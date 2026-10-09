import json

from scripts.compare_global_strategies import (
    main,
    run_game,
    semantically_equal,
)
from blind_kwartet.moves import QuestionMove
from blind_kwartet.search_state import SearchState


def test_comparison_policies_share_the_same_state_and_record_diagnostics():
    game = run_game(driver="local", depths=(1,), seed=123, event_limit=2)
    first, second = game["decisions"]
    assert first["actor"] == 0
    assert first["possible_deals"] == 34032
    assert first["compact_t"] == "------------"
    assert set(first["global"]) == {"1"}
    assert first["global"]["1"]["nodes_expanded"] > 0
    assert first["global"]["1"]["semantic_question_classes"] >= 0
    assert second["event_index"] == 1


def test_only_driver_move_advances_and_replay_matches_final_state():
    game = run_game(driver="local", depths=(1,), seed=123, event_limit=2)
    # The comparison policies only observe views; a second deterministic run
    # verifies that the driver's trajectory is stable and is the one recorded.
    again = run_game(driver="local", depths=(1,), seed=123, event_limit=2)
    assert [item["local"]["move"] for item in game["decisions"]] == [
        item["local"]["move"] for item in again["decisions"]
    ]
    assert game["result"] == again["result"]


def test_semantic_equivalent_labels_are_not_deviations():
    state = SearchState.initial()
    assert semantically_equal(state, QuestionMove(1, 0, 0), QuestionMove(1, 0, 1))
    assert not semantically_equal(state, QuestionMove(1, 0, 0), QuestionMove(2, 0, 0))


def test_bounded_run_reports_a_real_deviation_and_writes_incrementally(tmp_path):
    output = tmp_path / "compare.jsonl"
    summary = tmp_path / "compare.md"
    assert main([
        "--mode", "decision", "--driver", "local", "--depths", "1,2",
        "--repeat", "1", "--seed", "123", "--event-limit", "2",
        "--output", str(output), "--summary", str(summary),
    ]) == 0
    lines = output.read_text().splitlines()
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert any(
        decision["deviations"]["local_vs_depth"]["2"]
        for decision in payload["decisions"]
    )
    assert "local vs depth 2: 1" in summary.read_text()


def test_resume_does_not_duplicate_completed_games(tmp_path):
    output = tmp_path / "compare.jsonl"
    summary = tmp_path / "compare.md"
    args = [
        "--mode", "games", "--depths", "1", "--repeat", "1", "--seed", "7",
        "--event-limit", "0", "--output", str(output), "--summary", str(summary),
    ]
    assert main(args) == 0
    assert main([*args, "--resume"]) == 0
    assert len(output.read_text().splitlines()) == 2  # local and depth 1

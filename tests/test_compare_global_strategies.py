import json

import pytest

import scripts.compare_global_strategies as compare
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


def test_projection_backend_numba_parses_and_is_recorded(tmp_path):
    output = tmp_path / "compare.jsonl"
    summary = tmp_path / "compare.md"
    assert main([
        "--mode", "games", "--depths", "1", "--driver", "1",
        "--projection-backend", "numba", "--repeat", "1", "--event-limit", "0",
        "--output", str(output), "--summary", str(summary),
    ]) == 0
    payloads = [json.loads(line) for line in output.read_text().splitlines()]
    assert {payload["projection_backend"] for payload in payloads} == {"numba"}
    assert "projection backend: numba" in summary.read_text()


@pytest.mark.parametrize("driver", ["4", "5"])
def test_positive_arbitrary_driver_depth_parses(tmp_path, driver):
    output = tmp_path / f"compare-{driver}.jsonl"
    summary = tmp_path / f"compare-{driver}.md"
    assert main([
        "--mode", "games", "--depths", driver, "--driver", driver,
        "--repeat", "1", "--event-limit", "0",
        "--output", str(output), "--summary", str(summary),
    ]) == 0
    assert {json.loads(line)["driver"] for line in output.read_text().splitlines()} == {
        "local", driver,
    }


@pytest.mark.parametrize("driver", ["0", "-1", "not-a-depth", "1.5"])
def test_nonpositive_or_noninteger_driver_depth_is_rejected(driver):
    with pytest.raises(SystemExit):
        main(["--driver", driver])


def test_projection_backend_is_passed_to_global_search(monkeypatch):
    backends = []
    original = compare._GlobalSearch

    class SpyGlobalSearch(original):
        def __init__(self, *args, **kwargs):
            backends.append(kwargs["projection_backend"])
            super().__init__(*args, **kwargs)

    monkeypatch.setattr(compare, "_GlobalSearch", SpyGlobalSearch)
    run_game(driver="local", depths=(1,), seed=123, event_limit=1, projection_backend="numpy")
    assert backends
    assert set(backends) == {"numpy"}

import importlib.util
from pathlib import Path
import sys


_SCRIPT = Path(__file__).parents[1] / "scripts" / "explore_breadth.py"
_SPEC = importlib.util.spec_from_file_location("explore_breadth", _SCRIPT)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MODULE
_SPEC.loader.exec_module(_MODULE)
explore = _MODULE.explore


def test_breadth_depth_zero_has_one_initial_state():
    result = explore(max_depth=0, dedup="raw", emit=None)
    assert result.visited_count == 1
    assert len(result.states_by_depth[0]) == 1
    assert result.reports[0].newly_discovered == 1


def test_breadth_produces_successors_and_deduplicates_raw_states():
    result = explore(max_depth=1, dedup="raw", emit=None)
    assert result.raw_successors_generated > 0
    assert result.visited_count == 1 + len(result.states_by_depth[1])
    assert result.visited_count <= 1 + result.raw_successors_generated


def test_raw_breadth_exploration_is_deterministic():
    first = explore(max_depth=1, dedup="raw", emit=None)
    second = explore(max_depth=1, dedup="raw", emit=None)
    assert first == second


def test_canonical_dedup_does_not_retain_more_states_than_raw():
    raw = explore(max_depth=0, dedup="raw", emit=None)
    canonical = explore(max_depth=0, dedup="canonical", emit=None)
    assert canonical.visited_count <= raw.visited_count

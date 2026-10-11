# Global-search exact memoization handoff

## Implemented

Added per-search transposition-table memoization to `_GlobalSearch` in
`src/blind_kwartet/players.py`.

The memo key is:

```text
(state.D, state.T, state.actor, depth_remaining, naming_signature)
```

`state.T` is retained as the exact tuple of card overrides. SearchState
successor transitions already normalize redundant overrides. No compressed
projection, symmetry canonicalization, relabelling, approximate hash, disk
storage, or Numba was introduced.

`naming_signature` contains both `_SearchNaming.categories` and
`_SearchNaming.cards`. This is required because naming affects semantic
question classes, representative exact moves, and successor naming context.

Only fully evaluated terminal, leaf, no-action, and recursive nodes are
inserted. Exceptions such as diagnostic cutoffs cannot insert partial values.
Deterministic action ordering and answer tie-breaking are unchanged.

Memoization is easy to disable for A/B comparison:

```python
_GlobalSearch(SingleCategorySolver(), memo_enabled=False)
```

Each `_GlobalSearch` instance owns its table, so normal player decisions get a
fresh table. `clear_memo()` is available when a caller reuses an instance for
independent top-level searches.

## Diagnostics added

`_GlobalSearch` now reports:

- `search_calls`
- `memo_lookups`
- `memo_hits`
- `memo_misses`
- `memo_entries`
- `memo_hit_rate`
- `memo_hits_by_depth`
- `memo_entries_by_depth`
- existing node, leaf, terminal, branching, and semantic-pruning counters

These fields are also included in `TreeDecisionDiagnostic` for global-search
player decisions.

## Tests added

`tests/test_global_search_memo.py` covers:

- exact memoized/non-memoized equality at initial depths 1 and 2;
- selected move, returned value, and candidate-value equality;
- strategic YES/NO answer equality;
- reachable NO-answer, multi-question, and resolved-category states;
- naming-sensitive cache separation;
- proof that memo hits occur on a nontrivial search.

Focused verification passed:

```text
PYTHONPATH=src:. pytest -q tests/test_global_search_memo.py \
  tests/test_move_symmetry.py tests/test_compare_global_strategies.py
```

The existing focused global-search tests also passed before the handoff was
updated.

## Benchmark mode

Added:

```text
scripts/benchmark_global_memo.py
```

It compares memoization OFF versus ON for the initial state and the early
state after `P1 asks P2 A1 -> NO`, reporting runtime, nodes, recursive calls,
leaves, hits, entries, speedup, and exact-result equality.

Example:

```text
PYTHONPATH=src:. python scripts/benchmark_global_memo.py --depth 3
```

The requested depth-3 benchmark was started but interrupted before producing
results. No benchmark or pytest process remains running. Depth 4 is optional
via `--include-depth-4` and should not be added to the normal pytest suite.

## Caveat for follow-up

The implementation assumes the established SearchState contract that `T` is
normalized at strategic search boundaries. The memo key intentionally does
not normalize or compress state itself, avoiding any possibility of merging
states through an unproven representation.

No game rules, SearchState semantics, SingleCategorySolver, category
projection, compressed-search key, full-state canonicalizer, or live referee
behavior were changed.

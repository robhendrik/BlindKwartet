# Strategy-comparison runner

## Files changed

- `scripts/compare_global_strategies.py`
- `tests/test_compare_global_strategies.py`
- `codex_handoff.md`

The earlier semantic-search collision diagnostic remains below this handoff.
No game rules, `SearchState`, single-category solver, compressed-key logic, or
move-symmetry semantics were changed.

## CLI

The runner supports:

```text
--mode decision|games|both
--depths 1,2,3
--driver local|1|2|3
--repeat N
--seed N
--event-limit N
--output PATH
--summary PATH
--resume
```

`decision` follows one driver trajectory while comparing local and requested
global depths at every decision. `games` runs separate same-seed games for
local and every requested global depth. `both` does both forms. JSONL is
flushed after every completed game; `--resume` skips completed
`(driver, game_index, mode)` checkpoints.

## Comparison semantics

Every policy receives the same immutable `PlayerView` and `SearchState`.
`ComparisonPlayer` evaluates local policy and each requested `_GlobalSearch`
depth, records their moves/values/diagnostics, and returns only the configured
driver move to the existing `Game` loop. Answers continue through the existing
answer-selection semantics.

Question moves are compared through the existing
`semantic_question_representatives` machinery, so arbitrary labels such as
B1/B4 are not reported as strategic deviations. Target-player differences
remain meaningful.

## Output format

The JSONL record contains game result data and one decision record per stable
decision: event index, actor, `|D|`, compact T, unresolved categories, local
move/value, each global depth’s move/value, candidate root values, node and
branch counters, leaf evaluations, runtime, and local/depth deviation flags.

The Markdown summary reports games, scores, winners, event counts, deviation
counts, and chronological deviations with all compared moves and values.

## Verification run

Command:

```text
PYTHONPATH=src:. python scripts/compare_global_strategies.py \
  --mode decision --driver local --depths 1,2 --repeat 1 \
  --seed 123 --event-limit 2 \
  --output /tmp/strategy_compare.jsonl \
  --summary /tmp/strategy_compare.md
```

It completed successfully with two events. The first decision compared local,
depth 1, and depth 2 on `|D|=34032`; the second decision recorded the same
state view for all policies and found a real local/depth-2 answer deviation.
Only the local driver move advanced that trajectory. JSONL was written before
summary generation.

Mode-2/resume verification used `--event-limit 0`; it produced exactly three
records for local, depth 1, and depth 2, and a resumed invocation added no
duplicates.

## Tests

```text
PYTHONPATH=src:. pytest -q tests/test_compare_global_strategies.py
5 passed

PYTHONPATH=src:. pytest -q tests/test_compare_global_strategies.py \
  tests/test_move_symmetry.py tests/test_game_architecture.py
22 passed
```

Syntax compilation, `--help`, and `git diff --check` also passed.

## Suggested overnight commands

```text
PYTHONPATH=src:. python scripts/compare_global_strategies.py \
  --mode decision --driver local --depths 1,2,3 --repeat 1 \
  --seed 123 --output results/local_path_compare.jsonl \
  --summary results/local_path_compare.md
```

```text
PYTHONPATH=src:. python scripts/compare_global_strategies.py \
  --mode games --depths 1,2,3 --repeat 10 --seed 123 \
  --output results/depth_games.jsonl --summary results/depth_games.md \
  --resume
```

## Known performance considerations

The runner imposes no search timeout. Real global depth-2 evaluation is
already materially more expensive than depth 1; depth 3 is intended for the
user’s overnight run. Results are checkpointed only after a game completes,
so an interruption during one game repeats that game on resume.

# Semantic-search collision diagnostic

## Setup

This is a diagnostic-only rerun after global search move-symmetry pruning.
No game rules, `SearchState` semantics, compressed-key code, memoization, or
single-category solver code was changed.

The traversal started at `SearchState.initial()` and expanded exact legal
actions through `_GlobalSearch.search_actions()`. Question actions were
quotiented with the existing local naming symmetry; answers were still applied
through the authoritative exact `SearchState` transition. Quartet actions and
forced-quartet stabilization were retained.

Each unique stable state was keyed exactly as `(D, T, actor)`. A second map
grouped those states by the existing `CompressedSearchKey`. Collision classes
were checked with targeted exact cyclic-seat/category/card transforms. The
expensive 82,944-transform canonicalizer was used only during an initial spot
check; it was not used as the traversal key or exhaustively for every state.

The repository configuration has three players and three categories. Its
initial exact question frontier is therefore 24 questions, which prunes to two
semantic classes: `P1 asks P2 A1` and `P1 asks P3 A1`.

## Verification of old B1/B4 collision

After:

1. `P1 asks P2 A1 -> YES`
2. `P1 asks P2 A2 -> YES`

the exact state has 20 legal questions. The semantic representatives are:

```text
P1 asks P2 A3
P1 asks P3 A3
P1 asks P2 B1
P1 asks P3 B1
```

`P1 asks P3 B1` is present and `P1 asks P3 B4` is absent. Thus B1/B4 is
recognized as one first-card-in-a-new-category search branch, while P2/P3
remain distinct.

The previous B1/B4 collision is consequently not generated as two separate
search branches by the pruned traversal.

## Reachable compressed-key collision statistics

The complete depth-3 pruned traversal reached:

| Frontier / corpus | Unique exact states | Raw questions | Semantic classes | Pruned |
|---|---:|---:|---:|---:|
| depth 1 cumulative | 5 | 24 | 2 | 22 |
| depth 2 cumulative | 41 | 114 | 20 | 94 |
| depth 3 cumulative | 405 | 850 | 220 | 630 |
| depth-3 frontier only | 364 | — | — | — |

Grouping all 405 unique states by compressed key produced 37 collision
classes. The depth-3 frontier contained 29 classes; the remaining 8 were
cross-depth classes. All 37 classes were checked with exact current naming
relabelings:

```text
symmetry-equivalent classes: 37
genuine non-symmetry classes: 0
```

The first collision in the depth-3 frontier was the same semantic state
reached by resolving category A before introducing B versus introducing B
before resolving category A. Exact canonicalization confirmed that pair as a
valid relabelling. The other collision classes similarly differed only by
cyclic seat, category, or currently unnamed-card relabelling.

## First genuine collision, if any

No genuine collision was found in the tested corpus. Therefore there is no
pair of non-equivalent states for which the requested D/T, count-table,
projection, legal-move, leaf-value, or witness-deal dump would be applicable.

This is not a proof that the compressed key is globally exact. It is a result
for the complete reachable depth-3 tree generated by the current
symmetry-pruned search.

## Global-search performance after move pruning

These measurements use the real `SingleCategorySolver` leaf evaluator, not a
constant stub.

| Depth | Nodes expanded | Raw questions | Semantic classes | Pruned | Leaves | Runtime | Mean leaf time |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 5 | 24 | 2 | 22 | 4 | 2.335 s | 563.241 ms |
| 2 | 41 | 114 | 20 | 94 | 36 | 11.185 s | 283.131 ms |

For comparison, the earlier constant-leaf branching benchmark was:

```text
depth 1:  unpruned 49 nodes  -> pruned 5 nodes
depth 2:  unpruned 2209 nodes -> pruned 41 nodes
```

The real-leaf depth-1 selected root action was `P1 asks P2 A1`, with value:

```text
((0, 0, 0, 0, -3), (0, 0, 0, 0, -3), (0, 0, 0, 0, -3))
```

The real-leaf depth-2 selected root action was also `P1 asks P2 A1`, with
value:

```text
((0, 1, 0, 0, -2), (0, 0, 0, 0, -2), (0, 0, 0, 0, -2))
```

The corresponding `P1 asks P3 A1` root action returned the same value at both
depths; the selected representative is therefore seat-order tie-breaking,
not a claimed strategic distinction.

Depth 3 real-leaf search was not run to completion. The pruned structural
traversal itself reached 405 unique stable states, but real leaf evaluation at
that frontier is substantially more expensive.

## Implications for the Hall/count representation

The old apparent B1/B4 counterexample was arbitrary hidden labelling, not
strategic information: B1 and B4 were two labels for the first unnamed card
in a newly introduced category.

The diagnostic distinguishes:

1. arbitrary hidden labels in the 34,032-world labelled multiverse;
2. public distinctions created by named cards, transfers, constraints, and
   seating order; and
3. cross-category correlations that could be omitted by a compressed local
   notebook.

After quotienting category/card naming symmetry, no genuine cross-category
compressed-key collision was found in the tested depth-3 reachable corpus.
The current evidence therefore supports, but does not prove, the article’s
claim that count tables plus naming constraints and Hall matching capture the
strategically relevant state. It does not justify changing the compressed key
yet, because absence of a counterexample in this finite corpus is not a global
proof.

## Tests

The relevant test command was:

```text
PYTHONPATH=src:. pytest -q tests/test_move_symmetry.py \
  tests/test_compressed_search_key.py \
  tests/test_global_search_diagnostics.py
```

Result: `17 passed` before interruption in the existing expensive
canonicalization path; zero test failures were reported. The focused symmetry
suite independently passed `8 tests`. Syntax compilation also passed.

## Conclusion

The B1/B4 collision disappears from the symmetry-pruned search tree. In the
complete 405-state depth-3 diagnostic corpus, all 37 compressed-key collision
classes were valid semantic relabellings and none was a genuine loss of
strategic information. Real-leaf depth-2 search now expands 41 nodes and
completes in about 11.2 seconds on this environment.

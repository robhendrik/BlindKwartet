# Single-category solver handoff

## Result

Implemented the first isolated component for `strategy_player.md`: an exact
recursive adversarial solver for one four-card category. The solver uses an
81-world bitmap with base-three encoding and local relative players P1/P2/P3.

Implemented behavior:

- legal-ask filtering requires the actor to own another card in the category
  and not own the requested card;
- YES transfers the requested card to the asker and keeps the turn;
- NO leaves ownership unchanged and gives the turn to the respondent;
- impossible answer branches are ignored;
- P1 maximizes `WIN > OPEN > LOSS`, while P2/P3 minimize for P1;
- completed quartets return `WIN` for P1 and `LOSS` for P2/P3;
- no local legal move and recursion-stack recurrence return `OPEN`;
- completed states are memoized by exactly `(bitmap, actor)`;
- counters `nodes`, `memo_hits`, and `cycle_hits` are exposed.

## Files added

- `src/blind_kwartet/single_category_solver.py`
- `tests/test_single_category_solver.py`

The helper is not exported into the player API and does not integrate with
`Player`, `PlayerView`, `StateView`, or global multi-category state.

## Verification

- Focused tests: `9 passed` (`pytest -q tests/test_single_category_solver.py`).
- Full suite with the repository root import path: passed
  (`PYTHONPATH=src:. pytest -q`).
- Plain `pytest -q` still fails during collection because the existing
  `tests/test_verbose_random_game.py` imports `scripts`, while the project
  pytest configuration only adds `src` to `pythonpath`. This is unrelated to
  the new solver; adding the repository root to `PYTHONPATH` resolves it.

No Player subclass, StateView projection, multi-category strategy, or
count/NOT-owner compression was implemented.

## Behavioral Regression Diagnostics

Added realistic one-category entry coverage in
`tests/test_single_category_solver.py`:

- the canonical entry bitmap has exactly the nine requested P1 count triples
  and 38 possible worlds;
- the supplied six-observation line reduces the surviving entry worlds to the
  unique original assignment `(A1, A2, A3, A4) = (P3, P1, P2, P3)` and the
  final current state has all four cards with P3;
- the broad entry state has 8 legal first asks. Current diagnostic output
  reports `LOSS` for all 8, with `nodes=908`, `memo_hits=4562`, and
  `cycle_hits=434` (distance is not implemented);
- explicit tests cover impossible answer branches, recursion-stack cycles,
  delayed memoization until evaluation completion, and no legal local move.

The expanded focused suite passes: `13 passed`.

## Current-state Category Projection

The validated `SingleCategorySolver` remains unchanged. Added
`project_category_bitmap()` in `src/blind_kwartet/category_projection.py` as
the real-environment boundary for converting one global category into the
solver's 81-bit current-ownership bitmap.

Authoritative representation:

- `SearchState.possible_initial_deals` / `D` supplies surviving global worlds;
- `SearchState.current_owner()` resolves each card through the current-owner
  override tuple `T`, falling back to the corresponding initial deal;
- each surviving world is projected after those current transfers, and local
  duplicates collapse through `world_bit()` from the solver module.

Relative-player normalization maps the supplied active physical player to
relative P1/0, the next seat modulo three to P2/1, and the third seat to
P3/2. P2 and P3 are kept in seating order and are not mirrored.

Added `tests/test_category_projection.py` covering known ownership, global
world collapse, genuine local uncertainty, transferred current ownership,
active-player normalization, solver encoding compatibility, and the realistic
canonical observation prefix. The focused projection and solver tests pass:
`20 passed`. The full requested command `PYTHONPATH=src:. pytest -q` passes.

The current player-facing API supplies `PlayerView.state: SearchState`; there
is no separate `StateView` type in this repository. No Player subclass or
global-state integration was added. `strategy_player.md` remains the broader
architecture/design reference and does not mean every item in it is already
implemented.

## Recommended Next Task

Implement `SingleCategoryTreePlayer` as thin integration glue: evaluate the
legal moves supplied by the existing game environment by projecting their
category to the 81-bit bitmap and using `SingleCategorySolver`, selecting
`WIN > OPEN > LOSS`.

## SingleCategoryTreePlayer Integration

Implemented `SingleCategoryTreePlayer` in `src/blind_kwartet/players.py` and
re-exported it from `src/blind_kwartet/player.py` and
`src/blind_kwartet/__init__.py`.

The actual repository API is `Player.play(view: PlayerView) -> Move`. The
player only evaluates supplied `QuestionMove` actions. It first returns the
lowest-category supplied `QuartetMove`; otherwise it projects each ask's
category with `project_category_bitmap(view.state, move.category,
view.player_id)` and evaluates a local `LocalCategoryMove` with actor P1.
Physical targets use `(target - active_player) % 3`, preserving next-seat P2
and third-seat P3, and global card indices become local card indices by
subtracting `category * 4`.

Decision policy is exactly `quartet > WIN > OPEN > LOSS`. Question ties use
canonical `(category, target, card)` ordering. Answer views, which the current
Game can supply to a target player, are handled deterministically with YES
before NO so the player remains compatible with the existing game loop.

One `SingleCategorySolver` instance is reused across calls. Its recursion
stack is cleared at the end of each completed evaluation, and its memo key is
category-independent local `(bitmap, actor)`, so cumulative memo reuse is
safe. Lightweight cumulative counters and `last_evaluations` are exposed for
diagnostics.

Added `tests/test_single_category_tree_player.py` covering Player/API
compatibility, supplied-action selection, immediate quartets, WIN/OPEN/LOSS
priorities, deterministic ties, physical target normalization, non-first
categories, answer views, the broad 38-world LOSS state, and a short live
game. Focused integration tests pass: `9 passed`. The full requested
`PYTHONPATH=src:. pytest -q` suite passes.

Short demonstration with one tree player and two seeded random players,
limited to six events:

```text
end event_limit events 6
tree-selected question: category 0, target P2, card 0
tree candidate evaluations: 24 LOSS
diagnostics: nodes=1193 memo_hits=6647 cycle_hits=560
```

The broader original `strategy_player.md` remains the architecture/design
reference; it should not be read as claiming that every design item is
implemented.

## Recommended Next Research Step

Evaluate how `SingleCategoryTreePlayer` behaves in complete games and inspect
how often turns offer WIN, OPEN, or only LOSS options. Use those measurements
to decide what minimal multi-category lookahead is actually needed.

## Complete-game Benchmark Diagnostics

Added `scripts/benchmark_single_category_tree.py`. It runs deterministic
matches with the existing `Game`, `SingleCategoryTreePlayer`, and
`RandomPlayer` APIs, rotating the tree player through all three seats and
running an all-random baseline. CLI options are `--games`, `--seed`, and
`--event-limit`.

`SingleCategoryTreePlayer` now records lightweight per-call
`TreeDecisionDiagnostic` entries. These include supplied/evaluated question
counts, selected category/outcome, `|D|`, unresolved-category count,
`|D| == 1`, and per-decision solver node/memo/cycle deltas. Category-best
values are retained for cross-category diagnostics. The existing strategy
policy is unchanged.

Added `tests/test_benchmark_single_category_tree.py` for decision
classification, cross-category value-pair detection, and game observation
helpers. The benchmark-focused tests pass (`3 passed`); the full requested
`PYTHONPATH=src:. pytest -q` suite passes.

Small deterministic sample (`--games 2 --seed 123 --event-limit 6`):

```text
seat   games   wins   ties   losses   win_rate   mean_score   mean_events
P1        2      0      0       2     0.00%        1.00         5.00
P2        2      0      0       2     0.00%        0.00         6.00
P3        2      0      0       2     0.00%        0.00         6.00

decision summary: 4 question decisions
at least one WIN: 0 (0.00%)
no WIN but at least one OPEN: 0 (0.00%)
LOSS only: 4 (100.00%)
LOSS-only unresolved categories: 1=0, 2=2, 3=2
cross-category best values: all same=4; WIN/OPEN=0; WIN/LOSS=0; OPEN/LOSS=0
|D| == 1: 0.00%; |D| min/mean/max: 272 / 17152.00 / 34032
solver totals: nodes=3534 memo_hits=19634 cycle_hits=1424
tree games hitting event_limit: 6
```

The all-random baseline in this deliberately short sample had 2/2
event-limited games, so it is not a quality estimate. Larger default-style
runs were substantially slower because every tree turn evaluates many exact
category searches and did not complete within the available execution window.
The immediate research signal is that early turns are LOSS-only across all
categories, with no cross-category value disagreement observed in this
sample; longer event-limited batches are needed before drawing strategic
conclusions.

The next algorithmic step remains measurement: run longer bounded complete
games and inspect how often tree turns offer WIN, OPEN, or only LOSS options,
and how often different categories have different best local values, before
choosing minimal multi-category lookahead.

## Pythagoras termination rule

Implemented the global question rule: after normal asker/category/request-card
filtering, a question is legal only when the target owns the requested card in
at least one surviving current world (`D_yes != 0`). This is enforced by
`SearchState`, `QuestionContext` creation, `SingleCategorySolver` move
generation/evaluation, the modular `QuestionReferee`, and the legacy
reference `information_state` replay. No strategy, n-ply search,
canonicalization, or new memoization was added.

Updated `rules.md` to document condition 6, strategic YES/NO, forced YES, and
forced NO as unreachable under legal play. The existing `apply_answer` guard
still rejects impossible branches if an invalid context is manually
manufactured; no legal game path can create a forced-NO context.

Tests added/updated cover the post-NO reverse-question rejection, non-empty
YES branches for legal questions, local solver agreement, and legal replay
transcripts. Full result:

```text
103 passed in 63.11s
```

With `seed=123`, three identical tree players, `--repeat 2`, and
`--event-limit 200`, both runs terminated naturally:

- events: `24`; scores `(3, 0, 0)`; winner P1;
- distinct exact SearchStates: `13`;
- repeated-state encounters: `0`;
- final `|D|=1`, first reached after stable event 12;
- first WIN: P1 at event 5; P2/P3 never saw WIN;
- category switches: P1 `2`, P2 `1`, P3 `0`;
- graph had 12 edges and no cycle; repeated runs were identical.

The previous 4-state/2-state deterministic A1/NO cycle is gone. The new
state graph is `all_tree_cycle_after.dot`; Graphviz was unavailable, so render
it with `dot -Tpng all_tree_cycle_after.dot -o all_tree_cycle_after.png`.

## Exact SearchState cycle graph

Updated `scripts/benchmark_single_category_tree.py` with `--plot-state-graph`
and `--state-graph-output`. It records raw `(D, T, actor)` stable states,
aggregates repeated labelled transitions, reports cycle metadata, and writes
DOT without adding a Graphviz dependency.

Verified command:

```text
PYTHONPATH=src:. python -u scripts/benchmark_single_category_tree.py \
  --all-tree --repeat 1 --event-limit 20 --seed 123 \
  --plot-state-graph --state-graph-output all_tree_cycle
```

Result: 4 distinct states, first repeat `S2`, cycle entry event 4, cycle
length 2, cycle states `S2` and `S3`, with 7 repeated state encounters.
The transition table is `S0->S1` once, `S1->S2` once, `S2->S3` four times,
and `S3->S2` four times; every transition is the deterministic `A1 / NO`
exchange between P1 and P2. The game hit the event limit at 20 events with
scores `(0, 0, 0)` and final `|D|=6720`.

Generated artifact: `all_tree_cycle.dot`. Graphviz was unavailable; render
with `dot -Tpng all_tree_cycle.dot -o all_tree_cycle.png`.

Full verification after this change: `100 passed in 52.28s`.

## Strategic YES/NO answer evaluation

`SingleCategoryTreePlayer` now evaluates both legal answer branches only when
both YES and NO are supplied. Each branch is produced through the existing
`QuestionContext.apply_answer()` transition, stabilized, projected from the
answerer's physical seat, and solved with the answerer as local P1. The choice
uses `WIN > OPEN > LOSS`; equal values retain the existing NO tie-break.
Question selection and the Pythagoras rule were unchanged.

`TreeDecisionDiagnostic` now records answerer, asker/category/card, both local
outcomes, selected answer, and `strict` versus `tie` selection. The benchmark
supports `--answer-diagnostics`.

Final tests: `108 passed in 51.28s`.

All-tree (`seed=123`, two identical runs, event limit 200) remained stable:

- 24 events, natural termination, scores `(3, 0, 0)`, P1 winner;
- 13 distinct states, zero repeated states, final `|D|=1`;
- 4 strategic answers: 0 strict YES, 2 strict NO, 2 ties;
- all 2 ties selected NO; repeated runs were identical;
- answer diagnostics: P2 A1 LOSS/LOSS -> NO tie; P1 A2 LOSS/WIN -> NO;
  P2 B1 LOSS/LOSS -> NO tie; P1 B2 LOSS/WIN -> NO.

The regenerated graph is `all_tree_answer.dot`. No strict YES preference
occurred in this trajectory. The requested 500-game tree-vs-random rerun was
not practical: a 10-games-per-seat sample remained CPU-bound for over 100
seconds, so no fresh performance comparison is reported. The prior baseline
remains the only available comparison.

## Shallow global Max-N search

Added optional `SingleCategoryTreePlayer(global_depth=...)` and benchmark
`--global-depth`. Depth 0 retains the existing question and answer behavior.
Depth >0 searches complete stable transitions: question plus legal strategic
answer, or quartet declaration. The search returns one lexicographic value per
physical player and uses Max-N selection: the actor maximizes its component,
and the answerer maximizes its own component with NO on equal branch values.

Leaf values are `(terminal_rank, score, WIN_categories, OPEN_categories,
-LOSS_categories)`. Nonterminal states use rank 0; terminal states use exact
win/tie/loss rank followed by score. Existing `SingleCategorySolver` remains
the category leaf evaluator. No canonicalization or new memoization was added.

Full verification:

```text
PYTHONPATH=src:. pytest -q
114 passed in 53.95s
```

Depth-0 all-tree remains the established 24-event natural termination with
scores `(3, 0, 0)`. Depth-1/2 runs were attempted with the same seed and
event limit, but the required all-player, all-category leaf evaluation became
CPU-bound for several minutes in this environment and was stopped before a
reliable trajectory was captured. The dominant bottleneck is root branching:
each question evaluates both legal answer branches and three player-relative
category vectors. This is the expected target for the next memoization phase;
no memoization or symmetry work was added here.

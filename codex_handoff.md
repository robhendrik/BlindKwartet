# Milestone 3.5 Handoff

## Current Status

Milestones 1, 1.5, and 2 were already present and passing. `rules.md`,
`architecture.md`, and this handoff were read completely before
implementation. The exact slow reference symmetry/canonicalization layer is
now implemented over the pure `(D, T, actor)` rule/action layer.

The old referee and existing live engine remain in place as regression
references. No transposition tables, solver cycle handling, SearchPlayer,
minimax/Max-N, tournament, LLM, or aggressive canonicalization optimization
was added.

## Bottleneck Found

Profiling showed that dense states were dominated by construction/validation
of 165,888 transforms and repeated T packing. Sparse states were dominated by
per-deal Python allocation, deal-ID lookup, and transform/cache overhead. This
also explains why sparse |D|=2 can be slower than complete D: complete D is
invariant and only T must be mapped, while sparse D maps every surviving deal.
One cProfile run measured about 12.8s cold group construction and 5.7s sparse
deal mapping; process/cache warm-up affects these values.

## Optimization Design

`canonicalize_reference` preserves the exhaustive transformed-SearchState
oracle. `canonicalize` uses the same exact `(transformed_D, packed_T)` key on a
packed hot path. Legal deals also have a compact two-bit owner encoding and an
exact encoded-deal lookup. Transform members store their 12-card map once and
use validated construction. A bounded 65,536-entry packed deal cache is used;
the authoritative representation remains the dense D bitset.

Cheap ownership/category/T signatures are computed as a future pruning hook,
but no candidate is discarded from them: all 165,888 actor-normalized
transforms still receive the complete exact comparison. This conservative
choice protects semantics while establishing measurable acceleration.

## Exactness Validation

The optimized key was compared with the reference over fixed dense, sparse,
override, actor, and reachable-prefix states. Existing player/category/card/
combined symmetry, round-trip, and cross-deal-correlation tests remain in
place. The canonicalization file now has 9 tests and all comparisons passed.

## Benchmark

Representative default output (times vary by process/cache):

```text
165888 transforms
initial |D|=34032: reference 2.101522s, optimized cold 0.449155s,
  warm 0.447988s, speedup 4.69x
reachable-initial |D|=34032: reference 2.066325s, optimized cold 0.424220s,
  warm 0.368519s, speedup 5.61x
```

The benchmark reports `full_transforms=165888`. Sparse and replayed-small
oracle cases are available with `--include-slow` because they are much slower
in this runtime; no candidate-count reduction is claimed yet.

## Memory Use

No 165,888-by-34,032 table is allocated. Memory additions are compact owner
codes, cached actor-normalized transform tuples, 12-integer per-transform card
maps, and the bounded 65,536-entry deal cache.

## Files Added or Changed

- `src/blind_kwartet/deals.py`: existing Milestone 1 module. Enumerates the
  34,032 legal labelled initial deals and builds stable deal IDs and owner
  masks.
- `src/blind_kwartet/search_state.py`: added typed legal-question generation,
  transient answer contexts, YES/NO branch masks, quartet declarations,
  derived forced-quartet resolution, silence filtering, actor skipping,
  terminal scores, and invariant detection. Existing replay, adapter,
  normalization, and compatibility helpers remain.
- `src/blind_kwartet/search/transforms.py`: exact old-label-to-new-label
  player/category/rank transforms, inverse/composition, legal deal-ID mapping,
  bitset/T/actor transformation, and exhaustive actor-normalized group
  enumeration.
- `src/blind_kwartet/search/canonical.py`: exact canonical key `(D,
  packed_T)` and returned actual-to-canonical transform, plus canonical-state
  helper.
- `src/blind_kwartet/search/__init__.py`: search transform/canonicalization
  exports.
- `src/blind_kwartet/moves.py`: new `QuestionMove`, `AnswerMove`, `YES`,
  `NO`, and `QuartetMove` types for pure search actions.
- `src/blind_kwartet/exceptions.py`: added `SearchInvariantError` for an
  unresolved state with no legal action and `IllegalMove` for player choices
  outside the supplied view.
- `src/blind_kwartet/history.py`: immutable `QuestionEvent`, `AnswerEvent`,
  and `QuartetEvent` records used for public history and replay.
- `src/blind_kwartet/players.py`: immutable `PlayerView`, abstract `Player`,
  and seedable `RandomPlayer`.
- `src/blind_kwartet/player.py`: compatibility re-exports for player types.
- `src/blind_kwartet/game.py`: Game orchestration over stable SearchState,
  transient answer contexts, central legality, history, forced answers,
  terminal results, and defensive event limits.
- `src/blind_kwartet/result.py`: immutable `GameResult` with final state,
  scores, winners, end reason, seed, event count, and history.
- `src/blind_kwartet/__init__.py`: exports the new Game/action/player/result
  API.
- `scripts/play_random_game.py`: fixed-seed random-game demonstration.
- `tests/test_game_architecture.py`: mixed typed-action integration and Game,
  PlayerView, RandomPlayer, replay, score, skipping, and event-limit tests.
- `tests/test_search_actions.py`: focused Milestone 1.5 tests for legal
  questions, strategic/forced answers, quartets, silence-related legality,
  terminal ties, actor skipping, invariant failure, and monotone `D`.
- `tests/test_canonicalization.py`: group-size, card-label convention,
  transform round-trip, D popcount, player/category/card/combined symmetry,
  move round-trip, correlation preservation, and reachable-state tests.
- `scripts/benchmark_canonical.py`: reference timing baseline with an explicit
  `--include-large` opt-in for impractically slow large-D cases.
- `tests/test_search_state.py`: cleaned committed conflict markers while
  preserving the Milestone 1 regression coverage.
- `codex_handoff.md`: updated handoff.

## Implemented Behavior

- Enumerates exactly 34,032 legal initial deals and represents the surviving
  set as a bitset.
- Represents strategic state as `(D, T, actor)` with no hidden true deal.
- Resolves current ownership from initial ownership in `D`, overridden by
  public current-owner entries in `T`.
- Filters questions by actor turn, distinct players, family ownership by the
  asker, and not already owning the requested card.
- Filters YES to worlds where the target currently owns the card, and NO to
  worlds where the target does not.
- YES transfers the card to the asker and keeps the turn with the asker.
- NO leaves `T` unchanged and passes the turn to the target.
- `D` only shrinks; cards can be transferred back later.
- Replay supports the old zero-based `Question`/`Answer` event script while
  keeping pending-question protocol context out of `SearchState`.
- `from_game_state` adapts the existing factorized referee without deleting or
  replacing it, and rejects non-public per-card current ownership.
- Redundant `T` overrides are normalized away when `D` already implies them.
- Typed `QuestionMove`, `AnswerMove`/`YES`/`NO`, and `QuartetMove` actions are
  supported without putting pending-question context into `SearchState`.
- `legal_questions()` generates only actor-valid, unresolved-category,
  world-compatible questions and applies silence-as-information filtering.
- `QuestionContext` exposes `D_yes`, `D_no`, and exactly the currently legal
  strategic answer branches.
- YES/NO transitions apply transfer, actor progression, forced-quartet
  derivation, and cyclic actor skipping before returning a stable state.
- Voluntary quartet declarations filter `D`; impossible declarations fail.
- Resolved categories, forced quartets, quartet holders, scores, and terminal
  status are derived from current worlds represented by `D` and `T`.
- Unresolved states with no legal action for any player raise
  `SearchInvariantError`; terminal states can have equal scores, including
  `(1, 1, 1)`.
- `Game` asks the current seat's generic `Player` for a stable action, gives a
  strategic target a `PlayerView` containing both YES and NO when available,
  auto-applies forced answers, and records every question/answer/declaration.
- Full structured histories replay through `Game.replay()` and reproduce the
  live terminal `SearchState` exactly.
- `GameResult` reports terminal scores and all tied winners without historical
  quartet-order tiebreaking. A defensive `event_limit` result has no winners.
- The random demo reached `end=terminal scores=(0, 0, 3) events=50` with the
  fixed seeds in `scripts/play_random_game.py`.
- Canonicalization enumerates all 165,888 actor-normalized transforms and
  compares exact integer D plus exact packed T; no hash-only key is used.
- The canonical convention is `permutation[old_label] -> new_label`.
  A card-rank permutation is indexed by the old category before its category
  is moved.
- Deal IDs are transformed by mapping each full owner tuple through the one
  global transform and looking up the resulting legal deal ID. D is rebuilt by
  mapping every set bit; individual deal orbit occupancy is never used as a
  substitute for D.

No SearchPlayer, minimax/Max-N, tournament logic, transposition tables, or LLM
player was added.

## Tests

- Existing deal-universe, owner lookup, monotonicity, transfer-back, replay,
  old-referee, modular-referee, and engine tests remain relevant.
- Added the mixed question/YES/quartet typed-layer integration test and Game
  architecture regressions, alongside all Milestone 1/1.5 and old-referee
  tests.
- Canonicalization tests: 9 focused tests, including reference/optimized
  equivalence corpus and reachable-state checks.
- Final full result: `62 passed in 138.35s (0:02:18)` (`pytest -q`).

## Architecture / Rules Check

- The implementation now follows the architecture’s question rule that the
  asker must own another card in the category but not the requested card.
- `D` is monotone and `T` is a public current-owner override; physical cards
  may move back while knowledge does not grow.
- YES/NO branches remain consistency-based strategic choices; no branch-size
  probability or hidden deal is introduced.
- YES keeps the asker’s turn and NO passes to the target.
- `T` normalization now follows the architecture requirement.
- `rules.md` is present and agrees with the implemented semantics: no hidden
  deal, monotone `D`, public non-monotone transfers, silence, strategic
  answers, immediate forced quartets, turn retention/passing, cyclic skipping,
  and genuine ties.
- `architecture.md` requires history-free `(D,T,actor)` search state. Quartet
  resolution is derived from current ownership; no quartet history or score
  field was added.
- The pending question is represented only by transient `QuestionContext`, as
  allowed by the architecture’s search API.
- Existing legacy conflict markers in the Milestone 1 search test/state were
  removed; no unrelated referee or engine refactor was performed.
- `Game` delegates all legality and state transitions to `SearchState`; it
  does not implement rule logic or depend on concrete player subclasses.
- The only architecture-level compromise is that the new public history uses
  dedicated canonical event records rather than mutating the existing live
  `events.py` classes, whose player/name conventions differ. This preserves
  the old referee and keeps replay unambiguous.
- The old Milestone 3 benchmark remains useful as a historical baseline; the
  Milestone 3.5 benchmark now reports reference/optimized cold and warm times.
  The slow sparse/replayed oracle cases are opt-in with `--include-slow`.

## Remaining Questions

- The existing old referee does not model quartet declarations, so comparison
  for the mixed quartet integration path is limited to the new pure action
  layer; the old question/answer oracle remains intact.
- The existing factorized `GameState`/`GameEngine` remains separate from the
  new playable `Game`; a later migration can connect them without changing
  SearchState semantics.
- The benchmark’s large-D cases are not run by default; their exact timings
  remain an open performance-baseline question rather than a semantic gap.
- Can exact hierarchical signatures safely reduce the 165,888 candidate count
  without assuming a label ordering that is not proven by the deal IDs?
- Should packed deal mapping move to a compiled array/Numba layer after the
  algorithmic pruning design is validated?
- The slow sparse replayed oracle cases need a longer benchmark run before a
  final per-search-node performance decision.

## Recommended Next Step

Use the exhaustive and optimized canonicalizers as dual oracles to design and
validate exact candidate pruning. The smallest subsequent milestone is a
transposition-table-ready canonical-key interface, still without SearchPlayer
or minimax.

## Verbose Random-Game Demonstration

- Added `scripts/play_random_game_verbose.py`, a standalone reporting script;
  no engine, rules, SearchState, player, or canonicalization semantics were
  changed.
- Added `tests/test_verbose_random_game.py` for exact world-count entropy and
  information-gain helpers, plus fixed-seed game safety.
- Example fixed-seed output excerpt:

  ```text
  [event 1] P1 asks P3 for A1
    after asking: possible deals: 18064; entropy: 14.140830 bits;
      information gained: 0.913775 bits
  [event 2] P3 answers YES (strategic)
    after answer: possible deals: 9032; entropy: 13.140830 bits;
      information gained: 1.000000 bits
    transfer: A1 P3 -> P1
  Summary
  final quartet scores: (0, 0, 3)
  end reason: terminal
  total events: 50
  final possible deals: 1
  total information gained: 15.054604 bits
  ```

- Final test result: `64 passed in 172.21s (0:02:52)`.
- Question and answer information are reported separately by replaying each
  `QuestionEvent` through `apply_question` and each `AnswerEvent` through its
  pending `QuestionContext`. The current Game history does not record forced
  quartet resolutions as separate events, so the script derives them from
  resolved-category differences after stable transitions. It does not invent
  separate history records for them.

## Breadth-First State-Space Exploration

- Added `scripts/explore_breadth.py`, which explores stable
  `SearchState(D,T,actor)` nodes using complete question-plus-answer branches
  and quartet declarations. It supports `--max-depth`, `--dedup raw`,
  `--dedup canonical`, and `--show-nodes` without adding engine or solver
  behavior.
- Added `tests/test_explore_breadth.py` and `scripts/__init__.py` for focused
  deterministic/dedup coverage and script loading.
- Completed raw depth-1 example:

  ```text
  depth frontier newly cumulative terminal raw_edges branching
      0        1     48       49       0       48      48.00
      1       48      0       49       0        0       0.00
  ```

  The 48 depth-1 successors were all unique raw states; each had `|D|=9032`
  and mean legal-action count 23.50. A canonical depth-0 smoke run retained
  1 state, equal to raw mode. The raw depth-3 command was attempted and
  reached the depth-1 report with 2,076 newly retained states and 2,184 raw
  edges before being stopped while expanding the next generation; exact pure
  transition filtering is currently too slow for a practical depth-3 run.
- Final full result after this addition: `68 passed in 157.91s (0:02:37)`.
- Canonical dedup remains available and reports raw successors separately from
  canonical retained states, but depth-2 exploration was not run because the
  existing exhaustive canonicalizer is intentionally expensive per node.

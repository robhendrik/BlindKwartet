# Milestone 1.5 Handoff

## Current Status

Milestone 1 was already present and passing. `rules.md`, `architecture.md`,
and this handoff were read completely before implementation. The pure
search-facing rule/action layer is now implemented over `(D, T, actor)`.

The existing referee and live engine remain in place. No player, orchestration,
solver, canonicalization, tournament, or LLM work was added.

## Files Added or Changed

- `src/blind_kwartet/deals.py`: existing Milestone 1 module. Enumerates the
  34,032 legal labelled initial deals and builds stable deal IDs and owner
  masks.
- `src/blind_kwartet/search_state.py`: added typed legal-question generation,
  transient answer contexts, YES/NO branch masks, quartet declarations,
  derived forced-quartet resolution, silence filtering, actor skipping,
  terminal scores, and invariant detection. Existing replay, adapter,
  normalization, and compatibility helpers remain.
- `src/blind_kwartet/moves.py`: new `QuestionMove`, `AnswerMove`, `YES`,
  `NO`, and `QuartetMove` types for pure search actions.
- `src/blind_kwartet/exceptions.py`: added `SearchInvariantError` for an
  unresolved state with no legal action.
- `tests/test_search_actions.py`: focused Milestone 1.5 tests for legal
  questions, strategic/forced answers, quartets, silence-related legality,
  terminal ties, actor skipping, invariant failure, and monotone `D`.
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

No SearchPlayer, minimax/Max-N, tournament logic, canonicalization,
transposition tables, or LLM player was added.

## Tests

- Existing deal-universe, owner lookup, monotonicity, transfer-back, replay,
  old-referee, modular-referee, and engine tests remain relevant.
- Added focused action-layer coverage plus the existing Milestone 1 and old
  referee regression tests.
- Final full result: `44 passed in 11.65s` (`python -m pytest -q`).

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

## Remaining Questions

- The existing old referee’s event model remains separate from the new typed
  search actions; a future migration can add a direct adapter regression for
  quartet events.
- The live `GameState` still uses its existing factorized representation and
  pending-question field; the requested orchestration refactor is deferred.

## Recommended Next Step

Add pure successor/replay coverage for mixed question, answer, and quartet
transcripts against the old referee, then proceed to the smallest solver
preparatory milestone: cycle-safe successor traversal without
canonicalization or strategic players.

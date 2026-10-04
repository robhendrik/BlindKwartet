# Milestone 1 Handoff

## Current Status

The branch already contained a Milestone 1 implementation in committed files
`deals.py`, `search_state.py`, and `tests/test_search_state.py`. It enumerates
the exact default-game initial-deal universe, represents `(D, T, actor)`, and
provides replay and an adapter from the existing factorized referee.

The requested `rules.md` was not present in the repository or its parent
workspace, so it could not be read. `architecture.md` was read and used as the
authoritative structural reference. The worktree also contained a pre-existing
unrelated edit to `.codex/config.toml`; it was left untouched.

## Files Added or Changed

- `src/blind_kwartet/deals.py`: existing Milestone 1 module. Enumerates the
  34,032 legal labelled initial deals and builds stable deal IDs and owner
  masks.
- `src/blind_kwartet/search_state.py`: existing exact `(D, T, actor)` state,
  current-owner lookup, question/answer filtering, YES transfers, actor
  changes, replay, and old-state adapter. Fixed question legality to reject a
  requested card already owned by the asker, added card/deal validation, and
  normalized redundant public overrides after YES and adapter conversion.
- `src/blind_kwartet/referee.py`: added the same requested-card legality rule
  to keep the old brute-force comparison referee aligned with the architecture.
- `tests/test_search_state.py`: existing Milestone 1 coverage extended for
  owned-card rejection and `T` normalization; the transfer-back expectation
  now reflects normalized `T`.
- `tests/test_referee.py`: updated one stale expectation to reflect the
  architecture-consistent legality rule; the old referee remains present.
- `codex_handoff.md`: this handoff.

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

No SearchPlayer, minimax/Max-N, tournament logic, canonicalization,
transposition tables, or LLM player was added.

## Tests

- Existing deal-universe, owner lookup, monotonicity, transfer-back, replay,
  old-referee, modular-referee, and engine tests remain relevant.
- Added regression coverage for owned-card question rejection and normalized
  YES transfers.
- Final full result: `34 passed in 10.10s` (`python -m pytest -q`).

## Architecture / Rules Check

- The implementation now follows the architecture’s question rule that the
  asker must own another card in the category but not the requested card.
- `D` is monotone and `T` is a public current-owner override; physical cards
  may move back while knowledge does not grow.
- YES/NO branches remain consistency-based strategic choices; no branch-size
  probability or hidden deal is introduced.
- YES keeps the asker’s turn and NO passes to the target.
- `T` normalization now follows the architecture requirement.
- `rules.md` is missing, which is an unresolved repository discrepancy. The
  supplied rules in the task and `architecture.md` were used instead.
- Quartet declaration/forced-resolution behavior belongs to the existing live
  referee layer; the new `SearchState` does not yet expose quartet moves or a
  stable completed-category representation. This was left unchanged because
  quartet search was outside the requested Milestone 1 implementation scope.

## Remaining Questions

- Should the missing `rules.md` be restored to the branch, and should it be
  reconciled with `architecture.md` if they differ?
- Should a future search-facing adapter expose quartet actions and forced
  quartet resolution directly from `(D, T, actor)`?
- Should the live `GameState` eventually carry an explicit phase/pending
  question as described by `architecture.md`, or remain on the current
  pending-question field during migration?

## Recommended Next Step

Add a small search-facing legal-action layer for question, answer, and quartet
moves over `SearchState`, including invariant failures for unresolved
categories with no legal action. Leave strategy and optimization for later
milestones.

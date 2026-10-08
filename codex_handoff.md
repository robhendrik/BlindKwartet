# Global-search duplicate measurement handoff

Implemented measurement-only global-search diagnostics; no memoization, strategy, rules, or leaf evaluator changes.

## Files

- [players.py](/workspaces/BlindKwartet/src/blind_kwartet/players.py)
- [global_search_diagnostics.py](/workspaces/BlindKwartet/src/blind_kwartet/global_search_diagnostics.py)
- [measure_global_duplicates.py](/workspaces/BlindKwartet/scripts/measure_global_duplicates.py)
- [test_global_search_diagnostics.py](/workspaces/BlindKwartet/tests/test_global_search_diagnostics.py)

## Exact keys

- State: `(state.D, state.T, state.actor)`
- Search subproblem: `(state.D, state.T, state.actor, depth_remaining)`

Equality uses complete integer/tuple values. Compact `T` strings and sequential IDs are display-only.

## Results

Bounded real search, depth 3, 10 ms cutoff:

- Total visits: 2
- Unique states: 2
- State duplicate rate: 0%
- Unique state+depth keys: 2
- State+depth duplicate rate: 0%
- Cutoff results were discarded.

Monte Carlo, 100 depth-3 paths, seed `123`:

- Total visits: 400
- Unique exact states: 241
- Exact-state duplicates: 159 / 400 = 39.75%
- Unique state+depth keys: 241
- State+depth duplicates: 159 / 400 = 39.75%

By remaining depth:

- 3: 100 visits, 1 unique, 99% duplicate
- 2: 100 visits, 41 unique, 59% duplicate
- 1: 100 visits, 99 unique, 1% duplicate
- 0: 100 visits, 100 unique, 0% duplicate

Multiplicity histogram:

- Once: 205 states
- Twice: 16
- 3–5 times: 19
- >10 times: 1

Top repeated states included the initial state visited 100 times, plus depth-2 states visited four times each.

The 10,000-path sample was impractical because each exact transition scans the full 34,032-deal universe; the completed 100-path result is reported rather than extrapolated.

## Conclusion

Raw memoization appears potentially useful at shallow internal plies, especially depth 2, but most newly reached states remain genuinely distinct at deeper plies. The state+depth rate matched the exact-state rate in this sample, so there was no observed cross-depth reuse.

## Validation

`119 passed`.

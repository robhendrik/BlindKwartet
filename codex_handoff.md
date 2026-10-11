# BlindKwartet exact category-projection optimization report

## Implementation

Added an exact materialized owner table:

```python
INITIAL_OWNER[deal_id, card_id]  # numpy.uint8
```

It is deterministically constructed from the authoritative `INITIAL_DEALS`
tuples and has shape `(34032, 12)). `SearchState.D` remains the
authoritative exact surviving-world bitmask; the table is only a lookup view
of existing deal data.

Added explicit projection backends in
`src/blind_kwartet/category_projection.py`:

- `python`: unchanged reference implementation;
- `numpy`: exact owner-table lookup, override application, relative-player
  normalization, base-3 encoding, and 81-bit accumulation;
- `numba`: primitive integer kernel over exact surviving deal IDs, returning
  low/high 64-bit words for the 81-bit bitmap.

The NumPy and Numba paths derive surviving deal IDs exactly from `D`; they do
not replace or compress `D`. No SearchState object is passed into Numba.

Global search accepts:

```python
_GlobalSearch(..., projection_backend="python" | "numpy" | "numba")
```

The default remains `python` for conservative compatibility. Existing memo
keys, semantic pruning, tie-breaking, solver behavior, game rules, and referee
behavior are unchanged.

Optional benchmark-only timing counters report:

- surviving-ID enumeration;
- owner-table reads;
- override application;
- base-3 encoding;
- bitmap accumulation.

## Validation

Added focused tests covering:

- owner-table shape, dtype, and equality against all authoritative deal tuples;
- known and sampled deal IDs;
- initial, A1/NO, transfer, resolved-category, and small-`D` states;
- all categories and active players;
- bit-for-bit Python/NumPy equality;
- bit-for-bit Python/Numba equality when Numba is available.

Focused projection and global-search regression tests passed. The full pytest
run was started, but its runner session did not return a final summary after
the long-running suite; no pytest process remains running. No semantic
regression was observed in the completed focused tests.

## Projection microbenchmark

Command:

```text
PYTHONPATH=src:. python scripts/benchmark_category_projection.py \
  --projection-repeats 5 --backends python,numpy,numba
```

Representative results:

| State | `|D|` | NumPy speedup | Numba speedup |
|---|---:|---:|---:|
| Initial | 34,032 | 1.58x–1.80x | 1.76x–1.86x |
| A1/NO | 9,032 | 3.12x–3.27x | 2.37x–3.12x |
| Mid-transfer | 2,072 | 8.22x–9.20x | 8.59x–8.64x |
| Late | 1 | 161x–203x | 1,786x–1,805x |

All reported backend results were bit-for-bit equal to the Python reference.

Numba compilation was approximately:

- initial state: 0.8–0.9 seconds;
- A1/NO: approximately 0.04 seconds;
- mid/late states: already warmed in the same process.

The dominant residual cost in optimized projection is exact surviving-ID
enumeration. Owner-table access and encoding are comparatively small.

## Global-search benchmark

Memoization was ON throughout.

### Initial state, depth 3

| Backend | Runtime | Speedup vs Python | Nodes | Leaves | Memo hits | Memo entries | Selected move |
|---|---:|---:|---:|---:|---:|---:|---|
| Python | 247.95 s | 1.00x | 404 | 364 | 4 | 404 | P1 asks P2 A1 |
| NumPy | 48.00 s | 5.17x | 404 | 364 | 4 | 404 | P1 asks P2 A1 |
| Numba | 29.44 s | 8.42x | 404 | 364 | 4 | 404 | P1 asks P2 A1 |

All three returned the same value:

```text
((0, 0, 0, 0, -2), (0, 1, 0, 0, -2), (0, 0, 0, 0, -2))
```

### A1/NO state, depth 3

The optimized backends completed with identical results:

| Backend | Runtime | Nodes | Leaves | Memo hits | Memo entries | Selected move |
|---|---:|---:|---:|---:|---:|---|
| NumPy | 55.03 s | 1048 | 947 | 147 | 1048 | P1 asks P3 A1 |
| Numba | 54.22 s | 1048 | 947 | 147 | 1048 | P1 asks P3 A1 |

Both returned:

```text
((0, 0, 0, 1, -1), (0, 1, 0, 1, -1), (0, 0, 0, 1, -1))
```

The Python A1/NO reference run was started in the combined benchmark but
stopped after becoming impractically long, so no apples-to-apples wall-clock
speedup is claimed for that state. The earlier cProfile reference measurement
was approximately 380 seconds and is not used as a direct runtime comparison.

Benchmark command:

```text
PYTHONPATH=src:. python scripts/benchmark_category_projection.py \
  --projection-repeats 3 --global --global-depth 3 \
  --global-state a1-no --backends numpy,numba
```

## Recommendation

Make Numba the preferred production backend when the declared dependency is
available, with NumPy as the portable fallback and Python retained as a
reference/A-B backend.

The Numba path produced the largest initial global-search improvement and is
especially strong for small surviving-`D` states. NumPy is simpler to inspect
and still gives substantial speedups. A future default switch should be made
only after deciding how to handle environments without Numba and after a
separate full-suite run completes cleanly.

No compressed-state assumptions, symmetry canonicalization, approximate
hashing, or unrelated performance optimization was introduced.

## Extended engineering summary

### Why this optimization is safe

The optimization does not infer ownership, collapse worlds, or replace the
authoritative strategic state. Every projection still starts from the exact
surviving-deal mask `SearchState.D`. The new `INITIAL_OWNER` array is simply a
materialized copy of the existing immutable `InitialDeal.owner_by_card`
tuples:

```text
INITIAL_OWNER[deal_id, card_id] == INITIAL_DEALS[deal_id].owner_by_card[card_id]
```

The four selected category cards are read for every surviving deal. Public
current-owner overrides from `SearchState.T` are applied card-by-card exactly
as before. Physical owners are converted to active-player-relative owners with
the same cyclic mapping, then encoded using the existing base-3 world index.
The final result is still an 81-bit Python integer with exactly the same bit
meaning as the reference implementation.

The Numba implementation uses two `uint64` outputs because the result has 81
possible world bits. The low word contains bits 0–63 and the high word
contains bits 64–80; they are recombined into the same Python integer before
returning. This is an implementation detail only and is not a compressed
search key.

### Files changed

- `src/blind_kwartet/deals.py`
  - materializes `INITIAL_OWNER` as deterministic `numpy.uint8` data;
  - exports the table without changing `INITIAL_DEALS` or `D` semantics.
- `src/blind_kwartet/category_projection.py`
  - preserves the Python reference implementation;
  - adds NumPy and optional Numba exact paths;
  - adds lightweight optional projection timing counters.
- `src/blind_kwartet/players.py`
  - adds `projection_backend` and optional projection diagnostics to
    `_GlobalSearch`;
  - keeps Python as the default backend;
  - routes leaf evaluation through the selected exact projection backend.
- `tests/test_category_projection.py`
  - validates the owner table and all backend equality cases.
- `scripts/benchmark_category_projection.py`
  - runs projection microbenchmarks and global-search backend comparisons.
- `codex_handoff.md`
  - contains this implementation and benchmark record.

The earlier profiling harness and raw profiles remain available:

- `scripts/profile_global_search.py`
- `profile-results/global_search_initial_depth3_memoon.prof`
- `profile-results/global_search_a1-no_depth3_memoon.prof`

### Backend behavior

The Python backend remains the correctness reference and retains the original
`SearchState.surviving_deal_ids()` and `current_owner()` path. The NumPy path
uses exact set-bit extraction from `D`, indexed reads from `INITIAL_OWNER`,
vectorized override and relative-player operations, and a small Python loop
over the at-most-81 distinct world codes to form the Python integer bitmap.

The Numba path uses the same exact set-bit ID array and owner table, but moves
the four-card owner lookup, override selection, relative normalization, and
base-3 encoding into a primitive integer kernel. It does not JIT recursive
global search, answer selection, naming context, memoization, or SearchState
objects.

The backend is selected explicitly:

```python
project_category_bitmap(state, category, player, backend="python")
project_category_bitmap(state, category, player, backend="numpy")
project_category_bitmap(state, category, player, backend="numba")
_GlobalSearch(solver, projection_backend="numba")
```

Invalid backend names fail explicitly. Numba absence fails only when the
Numba backend is requested; the Python and NumPy paths remain usable.

### Equality coverage

The focused tests compare Python against NumPy and, when available, Python
against Numba for every category and active player in these states:

1. the initial state with all 34,032 deals;
2. after `P1 asks P2 A1 -> NO`;
3. a transfer state with multiple transferred cards;
4. a resolved-category state;
5. a late exact state with one surviving deal and explicit overrides.

The owner-table test compares the complete 34,032 × 12 table against the
authoritative deal tuples, not merely a small sample. The projection tests
require integer equality of the complete 81-bit bitmap, which is stronger
than comparing only decoded world sets.

### Strategic-result preservation

For initial depth 3, all backends produced:

```text
selected move:
QuestionMove(target=1, category=0, card=0)

value:
((0, 0, 0, 0, -2),
 (0, 1, 0, 0, -2),
 (0, 0, 0, 0, -2))

nodes=404 leaves=364 memo_hits=4 memo_entries=404
```

For the A1/NO depth-3 state, NumPy and Numba both produced:

```text
selected move:
QuestionMove(target=2, category=0, card=0)

value:
((0, 0, 0, 1, -1),
 (0, 1, 0, 1, -1),
 (0, 0, 0, 1, -1))

nodes=1048 leaves=947 memo_hits=147 memo_entries=1048
```

The node counts, leaf counts, memo statistics, selected moves, and returned
vectors remained unchanged. This confirms that the projection backend changes
only the cost of deriving local category bitmaps, not the strategic search
decisions.

### Performance interpretation

Projection speedups are strongest after the exact deal mask becomes sparse.
The original Python implementation repeatedly scans and materializes deal IDs,
then performs Python-level owner lookup for every card of every surviving
deal. The optimized paths remove dataclass/tuple traversal from the hot inner
loop. The remaining set-bit extraction from the large Python integer `D` is
still visible in the diagnostics, especially for the initial state.

The global-search speedup is lower than the isolated projection speedup can
suggest because global search also spends time in exact successor generation,
normalization, legality checks, quartet stabilization, and single-category
solver calls. Nevertheless, the initial depth-3 wall-clock reduction from
247.95 seconds to 29.44 seconds with Numba is material and preserves every
reported strategic result.

The A1/NO optimized runs completed in approximately 55 seconds. The Python
reference A1/NO run was stopped after becoming impractically long, so an
apples-to-apples wall-clock speedup for that state is intentionally not
claimed. The earlier cProfile reference measurement of approximately 380
seconds is useful for scale but is not a direct comparison because profiling
overhead changes absolute runtime.

### Recommendation and follow-up

The safest immediate deployment choice is:

1. retain Python as the explicit reference/A-B backend;
2. use Numba as the preferred production backend when the declared dependency
   is guaranteed;
3. use NumPy as the portable optimized fallback;
4. decide separately whether `_GlobalSearch` should default to Numba or select
   it through configuration.

Before changing the production default, run the complete test suite in a clean
process and verify the package’s supported environments all provide the
required numeric dependency. A fallback policy should be explicit rather than
silently changing strategic behavior.

The next highest-value optimization target is exact set-bit extraction from
large `D` masks and reuse of exact surviving-ID arrays within a projection
boundary. Any such cache must remain tied to the complete authoritative `D`
value and must not become a replacement state representation. Further
precomputation or Numba work should stay confined to integer-only projection
kernels; recursive object-heavy search orchestration is still not a promising
direct Numba target.

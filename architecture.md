# Blind Kwartet Architecture — v2

## Purpose

This document captures the intended software architecture for the Blind Kwartet project.

The design goal is to keep the following concerns cleanly separated:

- game rules;
- exact public information state;
- canonical search state and hashing;
- player strategies;
- LLM interaction;
- replay and history;
- tournament evaluation;
- analysis and visualization.

The first implementation target is:

- 3 players;
- 3 categories;
- 4 cards per category;
- no draw stack;
- all information is public;
- there is no hidden true deal;
- there is no bluffing;
- a move or answer is legal when it is compatible with at least one remaining possible initial deal.

The architecture should nevertheless remain general enough to support later variants such as 4 players and 4 categories.

---

# Core Principle

Blind Kwartet has no hidden "true deal" that the `Game` secretly knows.

Instead, the game keeps track of all legal **initial deals** that are still compatible with everything that has happened publicly.

Let

\[
D_t \subseteq D_0
\]

be the set of possible initial deals after event \(t\).

For the default 3-player × 3-category × 4-card game:

\[
|D_0| = 34\,032.
\]

The key invariant is:

\[
D_{t+1} \subseteq D_t.
\]

Public information can remove possible initial deals, but an eliminated initial deal can never return.

This monotonicity applies to knowledge about the **initial deal**. It does **not** mean that the physical card distribution is monotone: cards can be transferred and may later be asked back.

That distinction is fundamental:

\[
\boxed{\text{knowledge is monotone; current ownership need not be}}
\]

---

# Initial Deal Universe

There are 12 fully labelled cards:

```text
A1 A2 A3 A4
B1 B2 B3 B4
C1 C2 C3 C4
```

Each of the three players starts with four cards.

The number of fully labelled four-card deals is

\[
\frac{12!}{(4!)^3}=34\,650.
\]

An initial deal in which one player already holds all four cards of a category is excluded.

After removing those deals, exactly

\[
\boxed{34\,032}
\]

legal labelled initial deals remain.

These deals receive stable integer IDs:

```text
0 ... 34_031
```

The exact information state can therefore be represented by a bitset over these 34,032 initial deals.

A dense representation requires:

\[
34\,032\text{ bits}=4\,254\text{ bytes}.
\]

This is small enough to use directly as the exact basis of the search state.

---

# Top-Level Architecture

The outer structure follows the same pattern as QSeaBattle and PyCatan:

```text
GameConfig
    |
    v
Tournament
    |
    +---- creates many ----> Game
                              |
                              +---- GameState
                              |       |
                              |       +---- SearchState
                              |
                              +---- Referee
                              +---- History
                              +---- Players
```

The main objects are:

- `GameConfig`
- `GameState`
- `SearchState`
- `Referee`
- `Game`
- `Player`
- `Tournament`
- `GameResult`
- `History`

The important new distinction is between:

- `GameState`: everything needed to run the live game;
- `SearchState`: the minimal exact mathematical state needed for future strategic play.

---

# GameConfig

`GameConfig` contains static game parameters only.

Example:

```python
@dataclass(frozen=True)
class GameConfig:
    n_players: int = 3
    n_categories: int = 3
    cards_per_category: int = 4
    use_stack: bool = False
```

For the first version:

```text
n_players = 3
n_categories = 3
cards_per_category = 4
use_stack = False
```

Derived values include:

```python
total_cards = n_categories * cards_per_category
cards_per_player = total_cards // n_players
```

Rule code should avoid depending directly on the values `3`, `3`, or `4` where this can reasonably be generalized.

The optimized initial-deal and canonicalization code may initially be specialized for the 3×3×4 game.

---

# Two State Layers

## GameState

`GameState` is the state used by the live game engine.

Conceptually:

```python
@dataclass(frozen=True)
class GameState:
    search_state: SearchState

    phase: Phase
    pending_question: QuestionMove | None

    naming_map: NamingMap
```

It may additionally expose cached or derived presentation information such as:

```text
scores
completed quartets
active categories
human-readable current facts
```

These should not be duplicated as authoritative state if they can be derived exactly from `SearchState`.

`GameState` is useful because the live game naturally has a question phase and an answer phase.

## SearchState

The exact strategic state is:

\[
\boxed{\text{SearchState}=(D,T,\text{actor})}
\]

where:

- \(D\) is the subset of the 34,032 legal initial deals that remain possible;
- \(T\) is the public transformation from initial ownership to current ownership;
- `actor` is the player currently making the strategic choice.

Conceptually:

```python
@dataclass(frozen=True)
class SearchState:
    possible_initial_deals: int
    current_owner_override: tuple[int, ...]
    actor: int
```

This state contains no secret deal.

It also contains no subjective player beliefs.

---

# D — Possible Initial Deals

`D` is stored as a bitset.

Bit `i` is one iff initial deal `i` remains possible.

Conceptually:

```python
D: bitset[34032]
```

Initially:

```text
all 34,032 bits = 1
```

Every informative event filters the set:

```python
D_next = D & compatible_mask
```

Therefore:

\[
D_{t+1}\subseteq D_t.
\]

This bitset automatically preserves all correlations between categories and cards.

No separate cross-category constraint propagation is required for exactness.

---

# T — Public Ownership Transformation

A candidate initial deal tells us who originally owned each card.

Public transfers can change the current owner.

For each card, `T` stores either:

- no override: current owner is the owner in the candidate initial deal;
- a definite current owner resulting from public transfers.

For 12 cards:

```python
current_owner_override: tuple[int, ...]  # length 12
```

A compact encoding uses two bits per card:

```text
00 = no override
01 = current owner P1
10 = current owner P2
11 = current owner P3
```

Thus `T` requires only:

\[
12\times 2=24\text{ bits}=3\text{ bytes}.
\]

For candidate initial deal \(d\):

\[
\operatorname{owner}_{current}(c,d)=
\begin{cases}
T(c), & \text{if an override exists},\\
\operatorname{owner}_{initial}(c,d), & \text{otherwise}.
\end{cases}
\]

A card may be transferred more than once.

Only its current public owner must remain in `T`; information learned from previous transfers has already been captured by filtering \(D\).

---

# Normalizing T

The same strategic state should have only one raw representation where practical.

An override can become redundant.

Suppose `T[A1] = P2`, but after previous filtering every deal in \(D\) already has:

```text
initial_owner(A1) == P2
```

Then the override adds no information and can be reset to "no override".

Define:

```python
normalize_overrides(D, T)
```

to remove any override whose value is already implied by every deal in \(D\).

This is important because two different histories can otherwise produce distinct `(D, T)` encodings for the same current future-relevant state.

Normalization should run before hashing/canonicalization.

---

# Reconstructing Current Worlds

`D` and `T` together reconstruct every currently possible physical world.

For each `deal_id` in `D`:

1. take the corresponding initial ownership vector;
2. apply the public overrides in `T`;
3. obtain one possible current ownership vector.

Therefore no separate current-world list is needed.

The exact state is represented relative to the initial-deal basis rather than by repeatedly storing complete current worlds.

---

# Why the Old Per-Category Representation Is No Longer Authoritative

An earlier implementation represented each category separately.

For one 4-card category and three players there are:

\[
3^4-3=78
\]

legal detailed category worlds.

A separate count layer then propagated constraints between categories through the initial four-card hand sizes.

That representation remains mathematically useful, but it is no longer the preferred authoritative state.

The full-deal bitset \(D\):

- preserves all cross-category correlations exactly;
- removes the need for a separate fixed-point count propagation layer;
- provides a direct exact key basis;
- makes filtering simple bit operations.

The old 78-world and count representations may still be useful for:

- debugging;
- heuristics;
- visualization;
- explanatory output;
- blog figures;
- analysis of information gain.

They belong in the analysis/view layer rather than the core exact state.

---

# Precomputed Deal Masks

For fast filtering, precompute masks such as:

```text
initial_owner[player][card]
```

For 3 players and 12 cards this gives:

\[
3\times12=36
\]

bitsets.

Each mask contains all initial deals in which that player originally owns that card.

When a card has no override:

```python
D_yes = D & initial_owner[target][card]
D_no  = D & ~initial_owner[target][card]
```

When a card has an override, its current owner is already public and the branch may be forced without touching the bitset.

Additional masks may later be precomputed for common category-level predicates if profiling shows a benefit.

---

# Naming Map

Human names are mapped canonically as they appear.

Example:

```text
first category mentioned -> A
second category mentioned -> B
third category mentioned -> C
```

Within a category:

```text
first card mentioned -> 1
second card mentioned -> 2
third card mentioned -> 3
fourth card mentioned -> 4
```

Thus:

```text
Bloemen / Roos
```

might become:

```text
Bloemen -> A
Roos    -> A1
```

Semantic names are a presentation/history concern.

The exact search state uses canonical category and card labels.

The naming map need not be part of the strategic canonical key once all legal strategic actions can be expressed in canonical labels.

---

# Referee

The referee remains modular.

Suggested components:

```text
MappingReferee
QuestionReferee
AnswerReferee
QuartetReferee
TurnReferee
```

A coordinating `Referee` or `GameEngine` applies them to `GameState` / `SearchState`.

The old `HandCountConstraint` module is no longer required for exactness when `D` is authoritative.

It may remain as an analysis/checking module during migration.

---

# QuestionReferee

A question such as:

```text
P1 asks P2 for A3
```

is compatible only with current worlds in which:

1. P1 currently has at least one card in category A;
2. P1 does not currently have A3;
3. A is still available for play;
4. P1 is the current actor.

Because there is no hidden true deal, the act of asking itself is information.

The question filters \(D\) to the initial deals for which the question was legal in the corresponding current world.

If no deal survives, the question is illegal.

If at least one deal survives, the question is accepted and the reduced \(D\) becomes the new information state.

---

# AnswerReferee

There is no hidden deal that mechanically determines YES or NO.

The asked player chooses any answer that remains logically consistent.

For question:

```text
P1 asks P2 for A3
```

define:

\[
D_{\text{YES}}
=
\{d\in D:
\operatorname{owner}_{current}(A3,d)=P2\}
\]

and:

\[
D_{\text{NO}}
=
\{d\in D:
\operatorname{owner}_{current}(A3,d)\neq P2\}.
\]

There are three cases:

```text
YES non-empty, NO non-empty  -> P2 chooses YES or NO
YES non-empty, NO empty      -> YES is forced
YES empty, NO non-empty      -> NO is forced
```

The sizes of the branches are not probabilities.

A branch containing 50 possible initial deals is not less valid than one containing 5,000.

The answer is a strategic choice whenever both branches are non-empty.

## YES

For YES:

1. replace \(D\) by \(D_{\text{YES}}\);
2. publicly transfer the requested card to the asker;
3. update `T[card]`;
4. the asker retains the turn.

## NO

For NO:

1. replace \(D\) by \(D_{\text{NO}}\);
2. leave `T` unchanged;
3. the answerer becomes the next question actor.

---

# Question and Answer Nodes in Search

The live game naturally has two phases:

```text
QUESTION
ANSWER
```

Search does not necessarily need to store both as fully canonicalized transposition states.

A useful search structure is:

```text
QUESTION node
    actor chooses question / quartet
          |
          v
ANSWER choice
    target chooses YES or NO when both are consistent
          |
          v
next QUESTION node
```

The pending question can therefore be treated as transient search context.

Stable decision nodes can be canonicalized only after the answer and any forced resolution have completed.

This keeps the principal search key close to:

\[
(D,T,\text{actor}).
\]

---

# Quartet Rules

The project follows Kwartet semantics:

> A completed quartet must be announced immediately.

However, because there is no hidden true deal, a player may declare a quartet when that declaration is compatible with at least one remaining world.

The declaration itself then provides information.

## Voluntary Quartet Declaration

Suppose P1 declares:

```text
KWARTET A
```

Keep only deals in \(D\) for which, after applying `T`, P1 owns all four A cards.

If no deal survives, the declaration is illegal.

If deals survive, the quartet becomes logically established.

Because the cards remain in the player's hand, the owner and score contribution can be derived from the resulting exact state.

A separate authoritative `quartet_owner` variable is therefore unnecessary.

## Forced Quartet

If every surviving current world says that the same player owns all four cards of a category, that quartet is forced.

It should be resolved automatically.

A forced quartet is not a strategic branch.

## Silence Is Information

If the current actor could already have a completed mandatory quartet in some worlds but chooses another ordinary question instead, those worlds are inconsistent with the public action.

Therefore an ordinary question also implies:

```text
the actor did not have an undeclared mandatory quartet
```

and the corresponding deals must be removed before or as part of processing that move.

---

# Completed Categories and Scores

Completed categories do not need to be independent search-state variables if:

- completed quartet cards remain in the owner's hand;
- a declaration filters \(D\) until the quartet is established;
- forced quartets are automatically resolved.

Then category completion and quartet ownership are derivable from `(D,T)`.

Scores are likewise derivable as the number of completed categories owned by each player.

The live `GameState` may cache them for convenience, but cached values must agree with the exact state.

---

# Turn Progression

At a stable question node, `actor` is the player choosing the next question or quartet declaration.

After YES:

```text
actor remains the asker
```

After NO:

```text
actor becomes the answerer
```

During live play, `GameState.phase` and `pending_question` make the protocol explicit.

During deep search, the answer step may remain transient rather than becoming a separately hashed stable state.

---

# Asking Back Cards

Cards may be asked back later.

Example:

```text
A1: P2 -> P1 -> P2
```

provided the normal Kwartet asking rules are satisfied at each step.

No artificial "no return" rule is introduced merely to simplify search.

This means `T` is not monotone and the complete game graph can contain cycles.

Only \(D\) is monotone.

---

# Cycles

Because cards can move back and forth, it is possible in principle to revisit the same full strategic state:

\[
(D,T,\text{actor}).
\]

A cycle can only occur without gaining new initial-deal information along the cycle, because \(D\) can never grow.

The game rules currently do not forbid repetition.

Therefore cycle handling belongs in the solver, not in the game rules.

Search should detect repeated canonical states through:

- the transposition table;
- the current recursion/search stack;
- an explicit game-graph cycle policy.

The exact game-theoretic treatment of a genuinely infinite repetition can be chosen when the solver is implemented.

It should not be baked prematurely into the game rules.

---

# Move Types

Moves should be typed objects.

For example:

```python
@dataclass(frozen=True)
class QuestionMove:
    target: int
    category: int
    card: int

@dataclass(frozen=True)
class AnswerMove:
    yes: bool

@dataclass(frozen=True)
class QuartetMove:
    category: int
```

Typed moves simplify:

- validation;
- replay;
- serialization;
- canonical transformation;
- inverse transformation;
- search;
- testing.

---

# Legal Moves

Legal moves are generated centrally by the game/referee layer.

A `Player` does not implement rule legality.

Conceptually:

```python
legal_moves = referee.legal_moves(state)
```

A question or quartet declaration is legal when at least one consistent deal remains after applying all information implied by that action.

For answers, YES and NO are listed only when their corresponding deal subset is non-empty.

All player types therefore see the same legal action space.

---

# Search-State Canonicalization

Different labels can describe strategically identical states.

The search state should therefore be canonicalized before use as a transposition-table key.

The critical rule is:

> One single global relabelling must be applied consistently to the entire state.

It is not valid to canonicalize each possible deal independently.

The relations between the surviving deals contain information.

---

# Symmetry Group

At a stable decision node, map the current actor to canonical player P1.

After that anchoring, the remaining label symmetries are:

- swap the two non-active players: \(S_2\);
- permute the three categories: \(S_3\);
- independently permute the four card labels within each category: \((S_4)^3\).

Thus:

\[
G=(S_4\wr S_3)\times S_2
\]

with size:

\[
|G|
=
2!\times3!\times(4!)^3
=
165\,888.
\]

Every transform acts simultaneously on:

- player labels;
- category labels;
- card labels;
- all deal indices in \(D\);
- owner overrides in \(T\);
- moves.

---

# Initial Deal Orbits Are Not a Smaller Exact Basis

The 34,032 legal labelled initial deals fall into only 10 orbits under the actor-fixed symmetry group.

This does **not** mean that `D` can be replaced by 10 orbit bits.

An information state is a subset of labelled deals.

Two subsets can contain deals from exactly the same individual-deal orbit while differing in how those deals relate to each other.

That relational information affects future play.

Therefore:

```text
orbit type of each deal        -> useful summary
set of occupied deal orbits    -> lossy
full labelled subset D         -> exact
```

Symmetry should canonicalize the **whole subset** \(D\), not quotient each deal independently.

---

# Canonical Key

For a normalized stable state:

```python
state = normalize(state)
```

canonicalization considers the globally transformed versions:

\[
g(D,T,\text{actor}),\qquad g\in G.
\]

The actor is mapped to canonical P1.

The exact canonical representative may be chosen as the lexicographically smallest transformed pair:

\[
\boxed{
K(D,T)
=
\min_{g\in G}
\left(
g(D),g(T)
\right)
}
\]

where the same \(g\) is applied to both.

The canonicalizer returns:

```python
canonical_key, transform = canonicalize(state)
```

The transform is retained so that a move selected in canonical coordinates can be mapped back to the actual game labels.

---

# Canonical Transform

A transform must contain enough information to relabel both states and actions.

Conceptually:

```python
@dataclass(frozen=True)
class SymmetryTransform:
    player_perm: tuple[int, ...]
    category_perm: tuple[int, ...]
    card_perms: tuple[tuple[int, ...], ...]
```

It should support:

```python
transform_state(...)
transform_move(...)
inverse()
```

If search stores a best canonical move, the live game uses:

```python
actual_move = transform.inverse().apply(canonical_move)
```

---

# Reference and Optimized Canonicalizers

Canonicalization should be implemented in two stages.

## Reference implementation

First implement a deliberately simple exact version that tries all:

\[
165\,888
\]

actor-normalized transforms.

This version is too slow for deep search but serves as ground truth.

## Optimized implementation

Then add a pruned implementation using invariants such as:

- per-card/per-player frequencies across \(D\);
- category signatures;
- player/category count summaries;
- stabilizers of `T`;
- lexicographic prefix pruning.

The optimized implementation is accepted only if regression tests confirm:

```text
optimized_key(state) == reference_key(state)
```

over a large collection of reachable and randomly constructed valid states.

Numba or precomputed permutation tables can then be added if profiling justifies them.

---

# Deal-Index Transformations

A global relabelling induces a permutation of the 34,032 initial-deal IDs.

The implementation can precompute or compose these permutations.

Possible approaches include:

- full permutation table for every group element;
- factor tables for player/category/card generators;
- generator tables only;
- on-demand cached permutations.

The first implementation should prefer clarity and correctness over maximum speed.

The final choice should be benchmark-driven.

---

# Raw State Key Versus Canonical Key

Two key forms are useful.

## Raw key

Fast identity of an already labelled state:

```python
raw_key = (
    D,
    packed_T,
    actor,
)
```

This can cache expensive normalization/canonicalization work.

## Canonical key

Used for strategic transpositions:

```python
canonical_key = canonicalize(D, T, actor)
```

Equivalent relabelled states share the same canonical key.

A practical transposition table may use a 128-bit hash as an index, but exact code should retain enough information to detect or avoid hash collisions.

---

# Player Interface

All players use exactly the same interface.

`Game` must not know whether a player is:

- random;
- heuristic;
- deep-search;
- LLM-backed;
- human;
- hybrid.

Conceptually:

```python
class Player(ABC):

    @abstractmethod
    def play(self, view: PlayerView) -> Move:
        ...
```

`Game` only does:

```python
move = player.play(view)
```

No player-specific rule logic should appear in `Game`.

---

# PlayerView

A player receives everything required to choose a legal action.

Conceptually:

```python
@dataclass(frozen=True)
class PlayerView:
    player_id: int
    state: StateView
    legal_moves: tuple[Move, ...]
    history: tuple[GameEvent, ...]
```

A `SearchPlayer` can receive access to the exact `SearchState`.

A human or LLM player can receive a compact explanatory `StateView`.

All use the same underlying legal move set.

---

# Player Types

## RandomPlayer

Chooses randomly from legal moves.

Useful as:

- baseline;
- debugging opponent;
- tournament control.

## AlgoPlayer

Uses a hand-crafted heuristic.

Examples:

- information gain;
- quartet completion;
- blocking;
- turn retention;
- opponent modelling.

## SearchPlayer

Uses exact successor-state search.

Conceptually:

```python
for move in legal_moves(state):
    outcome = referee.transition(state, move)
    value = search(outcome)
```

Question moves may contain a nested strategic answer choice when both YES and NO are possible.

Search does not instantiate nested `Game` objects.

## LLMPlayer

Receives:

- compact state;
- legal moves;
- transcript/history;
- optional persona/instructions.

The model chooses among legal moves.

The LLM does not define legality.

## HumanPlayer

Uses the same `Player.play(view)` interface through a terminal, notebook, web UI, or other front end.

---

# Social Models and Trust

Subjective social interpretation does not belong in `SearchState`.

Examples:

```text
"P2 seems to help P1"
"P3 often blocks me"
"I trust P2"
```

are player-model facts, not objective game facts.

A trust-aware player may derive them from public `History`.

Therefore:

\[
\text{SearchState}
=
\text{objective future-relevant public state}
\]

while:

\[
\text{Player memory/model}
=
\text{subjective interpretation of behavior}.
\]

---

# History

`Game` maintains a structured public event history.

History is valuable for:

- social reasoning;
- trust models;
- LLM verbalization;
- replay;
- debugging;
- explanation;
- analysis;
- article examples.

Store structured events, not only transcript text.

For example:

```python
QuestionEvent(...)
AnswerEvent(...)
QuartetEvent(...)
```

A human-readable transcript can be generated from those events.

The distinction remains:

\[
\text{State}=\text{where are we now?}
\]

\[
\text{History}=\text{how did we get here?}
\]

History is not part of the exact strategic key unless a game rule is later introduced that explicitly depends on past occurrences.

---

# Replay

A complete game should be reproducible from:

```text
GameConfig
+ player/seat metadata
+ seed
+ structured History
```

Replay applies recorded events through the same referee used during live play.

A key regression invariant is:

```text
live final state == replay final state
```

Replay also provides a strong migration test for the new `(D,T)` representation.

---

# Game

`Game` orchestrates one complete game.

It owns:

```text
GameState
Players
Referee
History
GameConfig
```

Conceptually:

```python
while not game.is_over:
    player = game.players[game.current_actor]

    view = game.make_player_view(
        player_id=game.current_actor
    )

    move = player.play(view)

    game.apply(move)
```

`Game.apply(move)`:

1. sends the move to the referee;
2. obtains the next state or answer phase;
3. rejects illegal moves;
4. appends accepted events to history;
5. updates state;
6. resolves forced quartets;
7. checks game termination.

`Game` contains no player strategy.

---

# Illegal Moves

A move is illegal when the information implied by it leaves no compatible initial deal.

The low-level referee should raise:

```python
IllegalMove
```

and leave the previous state unchanged.

For tournaments, policy can be configurable.

A sensible default remains:

```text
illegal move -> player loses that game
```

rather than crashing the tournament.

Illegal-move details should be stored in `GameResult`.

---

# GameResult

A completed game returns a structured result.

For example:

```python
@dataclass(frozen=True)
class GameResult:
    game_id: int
    seat_scores: tuple[int, ...]
    winner_seats: tuple[int, ...]
    n_events: int
    end_reason: str
    seed: int
    history: tuple[GameEvent, ...] | None
```

The result uses seat numbers.

`Tournament` maps those seat results back to fixed competitor identities.

---

# Tournament

`Tournament` compares player strategies across many games.

Its most important role is to remove seat/order bias.

For three competitors, all:

\[
3!=6
\]

seat permutations can be used systematically.

Tournament should collect at least:

- games played;
- total score;
- average score;
- wins;
- ties;
- win rate;
- score by seat;
- average game length;
- illegal moves.

Useful later:

- branching factor;
- number of forced answers;
- information-state size \(|D|\) through time;
- number of canonical states visited;
- transposition-hit rate;
- number of quartet declarations;
- number of forced quartets;
- number and length of detected search cycles.

Seat-specific statistics should be retained even when seat rotation is used.

---

# Random Seeds and Reproducibility

Tournament owns a master random seed.

Each game receives a deterministic derived seed.

This supports exact reproduction of:

- RandomPlayer choices;
- stochastic heuristics;
- tournament schedules;
- simulation experiments.

LLM behavior may not be perfectly reproducible depending on provider and settings, but prompts, legal moves, model metadata, and selected outputs should still be logged.

---

# Player Identity Versus Seat

A fixed competitor is not the same as a temporary game seat.

For example:

```text
competitor:
    id = "search_depth_6"

temporary seat:
    P2
```

Tournament tracks competitors.

Game tracks seats.

This distinction remains explicit throughout statistics and replay.

---

# Strategy Metadata

Tournament results should record enough metadata to reproduce comparisons.

Examples:

```text
strategy name
strategy version
search depth
solver version
canonicalizer version
heuristic parameters
model name
temperature
prompt version
trust-model parameters
```

---

# Exact Search API

Search should work on pure state transitions wherever possible.

A useful low-level API is:

```python
legal_questions(state) -> tuple[Move, ...]

apply_question(state, move) -> QuestionContext

legal_answers(context) -> tuple[AnswerMove, ...]

apply_answer(context, answer) -> SearchState
```

or an equivalent abstraction that keeps the pending question transient.

Quartet declarations can directly map one stable decision state to the next after forced resolution.

The important requirement is that search does not need to instantiate or mutate a full `Game`.

---

# Search and Multi-Player Game Theory

Blind Kwartet has three strategic players.

Therefore deep search is not ordinary two-player minimax.

Possible later solver choices include:

- Max-N;
- paranoid search;
- equilibrium-oriented methods;
- explicit game-graph solution;
- policy/value learning.

The state architecture should not commit prematurely to one solver.

The exact canonical key and pure successor generation are shared infrastructure for all of them.

---

# Geometry / Analysis Layer

The geometric interpretation remains outside the core game engine.

Suggested modules:

```text
analysis/
    state_space.py
    information_geometry.py
    visualization.py
```

For each category, the initial count point:

\[
(n_1,n_2,n_3)
\]

lies on:

\[
n_1+n_2+n_3=4.
\]

Globally, initial category counts form a 3×3 matrix:

\[
M=
\begin{pmatrix}
n_{1A} & n_{1B} & n_{1C}\\
n_{2A} & n_{2B} & n_{2C}\\
n_{3A} & n_{3B} & n_{3C}
\end{pmatrix}
\]

whose rows and columns all sum to 4.

After dividing by 4, the continuous space is the Birkhoff polytope \(B_3\).

The integer game states live in the scaled polytope \(4B_3\).

There are 120 integer lattice points in \(4B_3\); excluding initial complete quartets leaves 87 legal labelled count matrices.

These count structures are useful for visualization and symmetry analysis, but they are not an exact replacement for the labelled-deal subset \(D\).

In particular:

- 16 canonical count structures remain if categories are permuted while players stay fixed;
- 10 remain when the active player is fixed and P2/P3 may also swap;
- these summaries do not preserve the relational information inside an arbitrary information state.

---

# Suggested Package Structure

```text
src/blind_kwartet/
    config.py

    deals.py
    state.py
    search_state.py
    moves.py
    events.py
    history.py
    result.py

    referee/
        mapping.py
        question.py
        answer.py
        quartet.py
        turn.py
        referee.py

    search/
        canonical.py
        transforms.py
        transposition.py
        solver.py

    players/
        base.py
        random_player.py
        algo_player.py
        search_player.py
        llm_player.py
        human_player.py

    analysis/
        category_worlds.py
        count_states.py
        state_space.py
        information_geometry.py
        visualization.py

    game.py
    tournament.py
```

Suggested responsibilities:

```text
deals.py
    enumerate and index the 34,032 legal initial deals
    precompute ownership masks

search_state.py
    D
    T
    actor
    normalization
    current-owner queries

search/transforms.py
    player/category/card relabellings
    transform state
    transform moves
    inverse transforms

search/canonical.py
    exact reference canonicalizer
    optimized canonicalizer

search/transposition.py
    raw-state cache
    canonical-key cache
    transposition table

analysis/*
    old 78-world/category-count representations
    geometric and explanatory views
```

---

# Migration From the Earlier Referee

The new representation should initially be introduced as an adapter, not as a destructive rewrite.

The earlier referee can remain the reference implementation while the new state is validated.

The migration path is:

```text
existing referee state
        |
        v
encode
        |
        v
SearchState(D,T,actor)
        |
        v
compare transitions
```

For many legal transcripts, verify after every event that:

- both representations retain the same legal initial deals;
- both imply the same current owners in every surviving world;
- both agree on legal questions;
- both agree on legal YES/NO answers;
- both agree on forced quartets;
- replay reaches the same final state.

Once this regression suite is strong, the `(D,T)` representation can become authoritative.

---

# Canonicalization Regression Tests

At minimum, test that equivalent relabellings give identical canonical keys.

Examples:

```text
state
swap categories A/B
-> same canonical key
```

```text
state
swap non-active players P2/P3
-> same canonical key
```

```text
state
swap cards A1/A3 globally
-> same canonical key
```

Also test non-equivalence:

```text
two states with different cross-world correlations
-> different canonical key
```

And move round trips:

```text
actual move
-> transform to canonical labels
-> inverse transform
-> original move
```

The optimized canonicalizer must be checked against the brute-force reference implementation.

---

# Architectural Invariants

1. **There is no secret true deal.** Reality is represented by the surviving set of legal initial deals.
2. **Possible initial deals only disappear.** \(D_{t+1}\subseteq D_t\).
3. **Current ownership may move in either direction.** Transfers, including asking a card back, are allowed.
4. **The exact strategic state is `(D,T,actor)`.**
5. **`D` preserves all cross-category correlations.** Count propagation is not part of the authoritative exact state.
6. **`T` stores only current public ownership overrides.** Earlier transfer history need not be retained in the search state.
7. **Redundant overrides are normalized before canonical hashing.**
8. **YES/NO is a strategic answer choice whenever both branches are consistent.** There is no probability weighting by number of deals.
9. **Forced answers and forced quartets are not strategic branches.**
10. **Quartet ownership and score are derived from the exact state where possible.**
11. **One global symmetry transform applies to the entire state.** Individual deals are never independently canonicalized.
12. **The labelled 34,032-deal basis remains exact.** Deal-orbit occupancy is only a lossy summary.
13. **The active player is canonicalized to P1 for search.**
14. **Canonicalization returns the transform as well as the key.**
15. **All players use the same interface.** Game does not know the strategy type.
16. **Players never communicate directly.** Interaction goes through Game.
17. **Legal moves are generated centrally.**
18. **History is structured and replayable.**
19. **History is not part of the strategic key unless a future game rule explicitly depends on history.**
20. **Natural card-return rules are preserved.** Cycles are handled by the solver rather than by artificial game restrictions.
21. **Search uses pure state transitions where possible.**
22. **Tournament separates competitor identity from seat and rotates seating.**
23. **Config, seeds, strategy metadata, events, and results should be serializable and reproducible.**

---

# First Implementation Milestone

The first complete architecture should support:

- 3 players;
- 3 categories;
- 4 cards/category;
- no stack;
- enumeration of exactly 34,032 legal initial deals;
- exact `SearchState(D,T,actor)`;
- dense deal bitset;
- packed owner overrides;
- override normalization;
- canonical naming;
- question legality;
- strategic YES/NO answers;
- public card transfers;
- voluntary quartet declarations;
- forced quartet resolution;
- silence as information;
- turn progression;
- legal-move generation;
- reference symmetry transforms;
- brute-force exact canonicalizer;
- inverse move transformation;
- RandomPlayer;
- deterministic/basic AlgoPlayer;
- HumanPlayer;
- replay;
- GameResult;
- Tournament with all six seat permutations;
- aggregate tournament report.

The next milestone should add:

- optimized canonicalization;
- canonical transposition table;
- cycle detection;
- SearchPlayer;
- solver experiments;
- search/tournament diagnostics.

LLM players, trust models, geometry visualizations, and larger game configurations can then be added without changing the basic `Game` / `Player` interface.

---

# Immediate Next Step

Implement the new search-state layer next to the existing referee:

```text
deals.py
search_state.py
search/transforms.py
search/canonical.py
```

Use the brute-force canonicalizer as a correctness oracle.

Then build a transcript-based regression suite that converts the existing referee state into `(D,T,actor)` after every event and verifies exact agreement.

Only after that should the old per-category/count representation be removed from the authoritative game-state path.

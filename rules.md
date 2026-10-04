# Blind Kwartet Rules

## Purpose

This document defines the game rules for the first exact version of **Blind Kwartet**.

It is intentionally separate from `architecture.md`:

- `rules.md` defines **what the game means**;
- `architecture.md` defines **how the software implements it**.

If implementation details and this document disagree, this document should be treated as the rule specification.

---

# 1. Game Setup

The first implementation uses:

- 3 players: `P1`, `P2`, `P3`;
- 3 categories: `A`, `B`, `C`;
- 4 cards per category;
- 12 cards total;
- 4 cards per player initially;
- no draw stack.

The fully labelled cards are:

```text
A1 A2 A3 A4
B1 B2 B3 B4
C1 C2 C3 C4
```

A player may not start with all four cards of one category.

Therefore there are exactly:

\[
34\,032
\]

legal fully labelled initial deals.

---

# 2. No Hidden True Deal

Blind Kwartet has **no secretly chosen true deal**.

Instead, the public game state represents the set of all legal initial deals that are still compatible with everything that has happened publicly.

Call this set:

\[
D.
\]

Initially, `D` contains all 34,032 legal initial deals.

Every public action may remove incompatible initial deals.

Once an initial deal has been eliminated, it never returns:

\[
D_{t+1} \subseteq D_t.
\]

This is the central information rule of the game.

---

# 3. Public Card Transfers

Although knowledge about the initial deal is monotone, the current physical ownership of cards is not.

A card may be transferred from one player to another after a YES answer.

A card may later be asked back, provided the normal asking rules are satisfied.

For example:

```text
A1: P2 -> P1 -> P2
```

is allowed.

Therefore:

- the set of possible initial deals can only shrink;
- the current ownership of cards may change in either direction.

No special anti-cycle rule is imposed.

---

# 4. Turn Order

Seat order is cyclic:

```text
P1 -> P2 -> P3 -> P1 -> ...
```

The current player is the **actor**.

At a stable decision point, the actor may:

- ask a legal question; or
- declare a legal quartet.

If the actor has no legal action, the turn passes to the next player in cyclic seat order who does have a legal action.

---

# 5. Asking a Question

A question has the form:

```text
P1 asks P2 for A3
```

A question is compatible with a possible current world only if:

1. the asker is the current actor;
2. the target is another player;
3. the category is unresolved;
4. the asker currently owns at least one card from that category;
5. the asker does not currently own the requested card.

Because there is no hidden true deal, asking the question is itself public information.

The question filters `D` to the initial deals whose corresponding current world makes that question legal.

If no initial deal remains, the question is illegal.

If at least one initial deal remains, the question is accepted.

---

# 6. Answering YES or NO

After a legal question, the asked player answers.

For a question such as:

```text
P1 asks P2 for A3
```

define:

\[
D_{YES}
=
\{d \in D :
P2 	ext{ currently owns } A3\}
\]

and:

\[
D_{NO}
=
\{d \in D :
P2 	ext{ does not currently own } A3\}.
\]

There are three cases:

```text
YES possible, NO possible   -> the asked player chooses YES or NO
YES possible, NO impossible -> YES is forced
YES impossible, NO possible -> NO is forced
```

An answer is legal if and only if its corresponding set of possible initial deals is non-empty.

The number of deals in a branch is **not a probability**.

For example, a branch containing 20 possible initial deals and one containing 2,000 possible initial deals are both simply legal strategic choices.

---

# 7. Effect of YES

After YES:

1. keep only `D_YES`;
2. transfer the requested card publicly from the target to the asker;
3. the asker retains the turn;
4. resolve all quartets that have become forced;
5. if the asker then has no legal action, pass the turn cyclically to the next player who does.

Example:

```text
P1 asks P2 for A3
P2 answers YES
A3 moves from P2 to P1
P1 remains the nominal actor
```

---

# 8. Effect of NO

After NO:

1. keep only `D_NO`;
2. no card is transferred;
3. the target becomes the next actor;
4. resolve all quartets that have become forced;
5. if that player has no legal action, pass the turn cyclically to the next player who does.

Example:

```text
P1 asks P2 for A3
P2 answers NO
P2 becomes the nominal actor
```

---

# 9. Quartets

A quartet consists of all four cards of one category held by the same player.

For example:

```text
A1 A2 A3 A4
```

held by `P1` is quartet `A` for `P1`.

A resolved quartet remains owned by that player.

Its cards do not need to be physically removed from the state.

Instead:

- that category becomes resolved/inactive;
- no further questions may be asked in that category.

---

# 10. Mandatory Quartet Resolution

A completed quartet must be announced/resolved immediately.

If all remaining possible current worlds agree that a player owns all four cards of a category, that quartet is **forced**.

Forced quartets are resolved automatically before the next strategic decision.

A forced quartet is not a strategic branch.

If several quartets become forced at the same time, resolve all of them before continuing play.

---

# 11. Voluntary Quartet Declaration

A player may declare a quartet even when the public information does not yet force it.

For example:

```text
P1 declares KWARTET A
```

The declaration is legal if at least one remaining possible current world has all four A cards at P1.

The declaration then filters `D` to precisely those worlds.

If no world remains, the declaration is illegal.

Thus a quartet declaration is itself public information.

---

# 12. Silence Is Information

Because a completed quartet must be announced immediately, choosing an ordinary action also conveys information.

If the actor asks another question instead of declaring a quartet, then all worlds in which that actor already had an undeclared completed quartet are incompatible with the action and must be removed.

In other words:

```text
ordinary move
```

also implies:

```text
the actor did not have a mandatory undeclared quartet
```

immediately before that move.

---

# 13. A Quartet Does Not End the Turn

Declaring or obtaining a quartet does **not** by itself end the player's turn.

Examples:

```text
P1 asks P2 for A4
P2 says YES
P1 now has quartet A
quartet A is resolved
P1 still has the turn
```

or:

```text
P1 declares quartet A
quartet A is resolved
P1 still has the turn
```

After resolving the quartet, the same player may continue if they still have a legal action.

---

# 14. No Active Options

A player may own cards but still have no usable cards because all categories represented in their hand have already been resolved.

If the current actor has no legal action:

1. do not end the game merely for that reason;
2. pass the turn to the next player in cyclic seat order;
3. continue until a player with a legal action is found.

This skipping is automatic and is not itself a strategic move.

---

# 15. Unresolved Categories Must Remain Playable

A normal game should not reach a state in which:

```text
one or more categories remain unresolved
```

but:

```text
no player has a legal question or quartet declaration
```

An unresolved category cannot be owned completely by one player, because then it would already be a quartet.

Therefore an unresolved category should still involve at least two players and permit continued play.

If the implementation reaches an unresolved state with no legal action for any player, this should be treated as an **invariant violation / bug**, not as a normal terminal condition.

---

# 16. End of the Game

The game ends when all categories have been resolved as quartets.

For the default game there are exactly three quartets in total.

The final score of each player is simply:

```text
number of quartets owned
```

Examples:

```text
2 - 1 - 0
1 - 1 - 1
3 - 0 - 0
```

---

# 17. Ties

There is **no historical tiebreaker**.

Players with the same number of quartets are genuinely tied.

Examples:

```text
1 - 1 - 1
```

is a three-way tie.

```text
3 - 0 - 0
```

has one winner and a tie for second place.

The order in which quartets were obtained is irrelevant to the final result.

This keeps final utility dependent only on the terminal state and not on game history.

---

# 18. History Does Not Affect Rule Legality

The public history is useful for:

- replay;
- explanation;
- debugging;
- LLM player behaviour;
- social/trust models;
- analysis.

But the ordinary game rules do not depend on how the current state was reached.

In particular:

- a card may be asked back;
- revisiting an earlier physical configuration is not forbidden;
- there is no repetition rule;
- quartet timing is not a tiebreaker.

For exact strategic play, two histories that lead to the same future-relevant state are equivalent.

---

# 19. Cycles

Because cards may be transferred back, the physical game graph may contain cycles.

For example, ownership may move:

```text
P1 -> P2 -> P1
```

while no additional initial deals are eliminated.

Cycles are therefore handled by the solver/search implementation.

They are **not** forbidden by an artificial game rule.

---

# 20. Canonical Names

Human-facing category and card names may be arbitrary.

Internally, names are mapped in order of first appearance:

```text
first category -> A
second category -> B
third category -> C
```

and within a category:

```text
first card -> 1
second card -> 2
third card -> 3
fourth card -> 4
```

For example:

```text
Bloemen / Roos -> A1
Bloemen / Tulp -> A2
```

These semantic names do not affect the game rules.

---

# 21. Legal-Move Principle

The engine, not the player implementation, determines legal actions.

A player receives a set of legal choices and selects one of them.

This applies equally to:

- human players;
- random players;
- heuristic players;
- search players;
- LLM players.

A move or answer that would leave zero compatible initial deals is illegal.

---

# 22. Stable Decision Point

For search and memoization, a stable decision point is reached only after:

1. the previous answer has been processed;
2. any YES transfer has been applied;
3. all forced quartets have been resolved;
4. players with no legal actions have been skipped;
5. the next actor with a legal choice has been identified.

At such a point, the strategic state can be represented by:

\[
(D,T,	ext{actor}).
\]

No quartet acquisition history or score history is required.

---

# 23. Rule Invariants

The implementation should enforce the following invariants:

1. There is no hidden true deal.
2. `D` is never empty in a legal game state.
3. Possible initial deals never return once eliminated.
4. Every public action filters or preserves `D`; it never enlarges it.
5. Current ownership is reconstructed from an initial deal plus public transfers.
6. Cards may be transferred back later.
7. A player may ask only from a category in which they currently hold at least one card.
8. A player may not ask for a card they currently hold.
9. YES is legal only if the target owning the card is possible.
10. NO is legal only if the target not owning the card is possible.
11. If both YES and NO are possible, the target chooses strategically.
12. YES keeps the turn with the asker.
13. NO passes the turn to the target.
14. A quartet is resolved immediately when forced.
15. A legal voluntary quartet declaration filters the possible initial deals.
16. Resolving a quartet does not end the turn.
17. Resolved categories are inactive for future questions.
18. Players with no legal action are skipped cyclically.
19. The normal terminal condition is that all categories are resolved.
20. Equal quartet counts are true ties.
21. History is not part of the game-theoretic state.
22. Cycles are permitted by the rules and handled by the solver.
23. An unresolved state with no legal action for any player is an invariant failure.

---

# 24. First-Version Scope

This rule document applies to the first implementation:

```text
3 players
3 categories
4 cards per category
no stack
```

Future versions may generalize the number of players/categories/cards, but such extensions must explicitly state whether any rule above changes.

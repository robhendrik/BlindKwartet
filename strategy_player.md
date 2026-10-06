Implement a new strategy player in the existing BlindKwartet game environment.

## Goal

Add a `SingleCategoryTreePlayer` child class of the existing `Player` class.

The current player API is approximately:

```python
Player.play(
    self,
    player_id,
    state: StateView,
    legal_moves: tuple[Move, ...],
) -> Move
```

Inspect the repository first and follow the actual current APIs/naming. Do not redesign the game engine, referee, state representation, or existing players. Use `RandomPlayer` and the existing game loop as references.

The new player should evaluate each legal move using an exact **single-category adversarial tree solver**.

This is deliberately NOT yet a multi-category search.

---

# Strategic interpretation

At entry to `play()`:

- the active physical player is the **hero**
- normalize this player locally to `P1`
- the next player in seating order is `P2`
- the remaining player is `P3`

This relative labeling remains fixed throughout a single-category solve.

Inside the local tree:

- `P1` is always the hero
- `P2` and `P3` cooperate against `P1`
- the internal actor can therefore be P1, P2, or P3
- after a YES, the asker keeps the turn
- after a NO, the respondent becomes the actor, according to the existing game rules

Do NOT renormalize the hero when the local turn changes.

---

# Local category state

Represent public knowledge about one category as an **81-bit bitmap**.

There are four cards in a category and three players, so a current ownership world is:

```text
(A1_owner, A2_owner, A3_owner, A4_owner)
```

with each owner in `{P1, P2, P3}`.

There are:

```text
3^4 = 81
```

possible current ownership worlds.

Use a deterministic encoding, for example:

```python
index = (
    owner_A1
    + 3 * owner_A2
    + 9 * owner_A3
    + 27 * owner_A4
)
```

where owners are `0, 1, 2`.

Bit `index` of the integer bitmap indicates whether that current world is still possible.

Important: these are **current card distributions**, not initial deals. If the global environment stores initial worlds plus transfers, project each surviving global world through the known transfers first, then create the category bitmap.

The category solver state is therefore essentially:

```python
(bitmap: int, actor: int)
```

where:

```text
actor = 0  -> hero/P1
actor = 1  -> P2
actor = 2  -> P3
```

Memoize on exactly this local state unless existing code requires one additional field for correctness.

Do not try to enumerate all `2^81` possible bitmaps. Only memoize states actually reached during recursive search.

---

# Projecting a global StateView to a category bitmap

Implement a helper that takes:

```python
state
category
hero_player_id
```

and returns the normalized 81-bit bitmap.

Physical players are mapped to relative players:

```text
hero              -> P1 / 0
next in seating   -> P2 / 1
remaining player  -> P3 / 2
```

Use the existing authoritative multiverse/state representation. Do not reconstruct game history if the repository already exposes sufficient current-world information.

---

# Single-category move semantics

The local solver only allows moves involving this category.

For an ask:

```text
asker asks respondent for card Ak
```

the act of making the ask is itself informative.

Filter the bitmap to worlds where the ask is legal:

1. asker owns at least one card of this category
2. asker does NOT own the requested card
3. preserve any other legality rules already implemented by the game environment

Then split the surviving bitmap into possible answers.

## YES branch

YES is possible in worlds where the respondent currently owns the requested card.

For every such world:

```text
requested card transfers respondent -> asker
```

The asker remains actor.

Map the resulting worlds back to the 81-world bitmap and deduplicate automatically through the bit representation.

## NO branch

NO is possible in worlds where the respondent does not own the requested card.

No card transfers.

The respondent becomes actor.

Impossible branches are ignored.

Where practical, reuse existing rule/transition helpers rather than creating a second inconsistent implementation of the game rules.

---

# Outcomes

Define:

```python
class CategoryOutcome(Enum):
    WIN = ...
    OPEN = ...
    LOSS = ...
```

Meaning from the fixed hero/P1 perspective:

### WIN

P1 can force the quartet even if P2 and P3 cooperate against him.

### LOSS

P2/P3 can force the category away from P1.

It does not matter which coalition player eventually receives the quartet.

### OPEN

The single-category model cannot force either conclusion.

Typical reasons:

- a cycle
- current actor has no legal move in this category and would have to switch category in the real game
- play leaves the locally resolvable part of the category

Do NOT interpret OPEN as LOSS.

---

# Recursion

Create a separate testable helper, e.g.:

```python
SingleCategorySolver
```

Conceptually:

```python
solve(bitmap, actor) -> CategoryResult
```

where `CategoryResult` should at minimum contain:

```python
outcome: CategoryOutcome
```

Preferably also:

```python
distance: int | None
best_move: local move | None
```

Distance is useful for tie-breaking:

- shortest forced WIN is preferable
- longest forced LOSS is preferable

But correctness of WIN/OPEN/LOSS is more important than sophisticated distance handling.

---

# Adversarial choice

At a P1 node:

```text
P1 chooses the best available move
```

with ordering:

```text
WIN > OPEN > LOSS
```

At a P2 or P3 node:

```text
coalition chooses the worst available move for P1
```

with ordering:

```text
LOSS < OPEN < WIN
```

P2 and P3 are therefore cooperating against the fixed hero.

---

# Evaluating an ask

A move may have a YES branch, a NO branch, or both.

The result of a move is the worst feasible answer branch for P1.

Equivalent truth table:

```text
YES       NO        MOVE RESULT
--------------------------------
WIN       WIN       WIN
WIN       OPEN      OPEN
OPEN      OPEN      OPEN
WIN       LOSS      LOSS
OPEN      LOSS      LOSS
LOSS      LOSS      LOSS
```

If only one branch is feasible, use that branch.

In other words:

```python
if all(feasible branches are WIN):
    move = WIN
elif any(feasible branch is LOSS):
    move = LOSS
else:
    move = OPEN
```

---

# Quartet handling

Use the existing game rules for quartet declaration.

A forced/valid quartet by P1 is terminal:

```text
WIN
```

A forced/valid quartet by P2 or P3 is terminal:

```text
LOSS
```

Remember that the existing BlindKwartet rules require a completed quartet to be announced immediately. Reuse existing helpers if available so this behavior remains consistent with the main game environment.

---

# Cycles

Cycle detection is required from the beginning.

Maintain separately:

```python
memo: dict[(bitmap, actor), CategoryResult]
recursion_stack: set[(bitmap, actor)]
```

Behavior:

```python
if key in memo:
    return memo[key]

if key in recursion_stack:
    return OPEN
```

Do not memoize a partially evaluated recursion-stack state as OPEN merely because one path reached it; only memoize completed state evaluations.

---

# No local move

If the current actor cannot make any legal move in this category and has no quartet:

```text
return OPEN
```

In the real game the player would switch category, which is deliberately outside this solver.

---

# SingleCategoryTreePlayer

Add a new `Player` subclass using the solver.

The main `play()` logic should roughly be:

```python
def play(self, player_id, state, legal_moves):

    # Immediate quartet move always wins/takes precedence.
    for move in legal_moves:
        if move is a valid quartet declaration:
            return move

    evaluated = []

    for move in legal_moves:
        category = category_of(move)

        bitmap = project_category_bitmap(
            state=state,
            category=category,
            hero_player_id=player_id,
        )

        result = solver.evaluate_root_move(
            bitmap=bitmap,
            move=move converted to relative P1/P2/P3 form,
        )

        evaluated.append((move, result))

    wins = [x for x in evaluated if x.result.outcome == WIN]
    if wins:
        return deterministic best WIN
        # Prefer shortest forced win if distance is implemented.

    opens = [x for x in evaluated if x.result.outcome == OPEN]
    if opens:
        return deterministic best OPEN

    # Everything locally loses.
    return deterministic LOSS move
    # Prefer longest distance-to-loss if implemented.
```

The player evaluates the legal moves already supplied by the game environment. It must never return an illegal move.

Use deterministic tie-breaking so tests and tournaments are reproducible.

Do not add multi-category lookahead yet.

---

# Performance

Because there are only 81 current ownership worlds per category, precompute useful masks/tables where this simplifies the implementation, for example:

```python
OWNER_MASK[card][player]
PLAYER_HAS_ANY_MASK[player]
```

A transfer can also use a precomputed mapping:

```python
TRANSFER_INDEX[asker][respondent][card][world_index]
```

Avoid premature optimization beyond this.

Expose solver statistics if convenient:

```python
nodes_evaluated
memo_hits
cycle_hits
```

These will be useful for understanding whether the local trees remain small.

---

# Tests

Add focused unit tests without changing existing tests.

At minimum cover:

1. bitmap encoding/decoding of all 81 worlds
2. global-state/category projection
3. YES filters correctly and transfers the requested card
4. NO filters correctly and passes actor to respondent
5. the legality of the ask itself filters impossible worlds
6. move with `WIN/WIN` branches => WIN
7. move with `WIN/OPEN` => OPEN
8. move with `WIN/LOSS` => LOSS
9. hero quartet => WIN
10. coalition quartet => LOSS
11. repeated `(bitmap, actor)` on recursion path => OPEN
12. no legal move in the category => OPEN
13. memoization gives the same result without re-expanding the state
14. `SingleCategoryTreePlayer.play()` always returns one of the supplied `legal_moves`
15. existing `RandomPlayer` and current game tests still pass

Also add a regression test for the canonical one-category line discussed below if it can be represented cleanly with the current environment:

```text
P1 asks P2 for A1 -> NO
P2 asks P3 for A1 -> YES
P2 asks P3 for A2 -> NO
P3 asks P1 for A2 -> YES
P3 asks P2 for A1 -> YES
P3 asks P2 for A3 -> YES
P3 calls quartet
```

This line identifies the original distribution:

```text
P1: A2
P2: A3
P3: A1, A4
```

and should be consistent with the adversarial single-category solver.

Do not hard-code this line; it is only a regression example.

---

# Scope discipline

For this task:

- DO implement the one-category exact bitmap solver
- DO implement memoization and cycle detection
- DO implement `SingleCategoryTreePlayer`
- DO add tests
- DO preserve existing APIs wherever possible

Do NOT:

- implement the full multi-category minimax tree
- redesign the multiverse representation globally
- add new game rules
- add heuristic archetypes yet
- attempt to enumerate `2^81` belief states
- optimize canonicalization beyond what is necessary for this player

After implementation, run the full test suite and give a concise summary of:

1. files added/changed
2. exact solver state/key used
3. tie-breaking behavior
4. tests added
5. full test-suite result
6. a small demonstration game using `SingleCategoryTreePlayer`, including solver node/memo/cycle statistics if available
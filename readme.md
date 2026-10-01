# Blind Quartets

Exploring the mathematics and algorithms behind **Blind Quartets**
(also known as *Quantum Happy Families* / *Quantum Go Fish*).

The unusual rule is that the cards do not need to have a predetermined
identity during play. Players may answer questions in any way that remains
consistent with some possible initial deal.

This repository explores that idea computationally.

## First Experiment

We begin with a deliberately small game:

- 3 players
- 3 families
- 4 cards per family
- 12 cards in total
- 4 cards per player

The cards are labelled generically:

```text
A1 A2 A3 A4
B1 B2 B3 B4
C1 C2 C3 C4
```

Rather than trying to derive consistency constraints symbolically, we
enumerate every legal initial deal.

For a given game transcript, every candidate initial deal is replayed.
Whenever a question or answer is incompatible with that candidate, the
candidate is eliminated.

The remaining initial deals form the **information state** of the game.

## Key Idea

The initial deal never changes.

Cards can move during play:

```text
initial deal
     |
     v
question
     |
answer YES
     |
A2: P3 -> P1
     |
next question
     |
...
```

For each candidate initial deal, we therefore distinguish between:

- the immutable **initial ownership** of every card;
- the **current ownership** resulting from transfers during the game.

A transcript is legal if at least one initial deal can reproduce the
complete sequence of events.

## Information-State Equivalence

Two different game histories are informationally equivalent if they leave
exactly the same set of possible initial deals.

If

```text
S(H1) = S(H2)
```

then histories `H1` and `H2` contain the same information about the
original deal.

In the brute-force implementation, an information state can therefore be
represented simply as a set of surviving initial-world IDs.

This also gives us a natural hashable representation for later search
algorithms.

## Roadmap

The project will proceed in stages:

1. Enumerate all legal initial deals.
2. Replay questions, answers, and card transfers.
3. Detect illegal transcripts.
4. Explore information-state equivalence.
5. Generate all legal moves from a game state.
6. Search the game tree.
7. Explore multiplayer strategy and kingmaker situations.
8. Add different assumptions about trust and adversarial behaviour.
9. Optionally use language models to turn algorithmic decisions into
   natural game dialogue.

The initial brute-force implementation is intentionally simple. It serves
as a reference against which more efficient algorithms can later be
tested.

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install development dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

Run the tests:

```bash
python -m pytest
```

## Background

The game is related to Blind Quartets and to variants that have circulated
under names such as *Quantum Happy Families* and *Quantum Go Fish*.

Despite the playful use of the word "quantum", the project does not assume
that the game implements quantum mechanics. The interesting mathematical
question is whether a sequence of statements remains consistent with at
least one possible underlying classical deal.
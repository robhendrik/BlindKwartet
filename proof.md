# Exact compressed representation of Blind Kwartet

## Theorem

For Blind Kwartet with three players, three categories of four cards, and the rules stated below, the information contained in the full multiverse of possible labelled initial deals can be represented exactly throughout the game by:

1. a set of possible **category-count matrices**;
2. a relation specifying which **named cards could initially have belonged to which players**;
3. the publicly known transfers of named cards;
4. the current turn, completed quartets, and other public game state.

No additional correlations between unresolved card identities need to be stored.

For any surviving count matrix, compatibility between the card names and the available player/category slots is a bipartite matching problem. Hall's marriage theorem therefore gives an exact test of whether that count matrix has at least one realization.

---

## 1. Definitions

There are three players $P_1,P_2,P_3$ and three categories $A,B,C$, each containing four cards:

$$
A1,\ldots,A4,\qquad
B1,\ldots,B4,\qquad
C1,\ldots,C4.
$$

These canonical labels may be imagined to exist from the start. During actual Blind Kwartet play, their human-readable names may only be invented when first mentioned.

A **deal** $d$ assigns each of the twelve labelled cards to one of the three players, four cards per player.

A **category-count matrix**

$$
C=(c_{pc})
$$

records how many cards of category $c$ player $p$ initially holds.

Therefore

$$
\sum_c c_{pc}=4
$$

for every player and

$$
\sum_p c_{pc}=4
$$

for every category.

An initial deal containing a complete quartet is excluded, so initially

$$
c_{pc}<4.
$$

There are 34,032 such labelled initial deals.

---

## 2. The invariant

After any public game history $h$, let

$$
W_h
$$

be the set of fully labelled initial deals still consistent with that history.

We claim that there exist:

- a set $\mathcal C_h$ of allowed category-count matrices; and
- a relation

$$
E_h\subseteq
\{\text{card names}\}\times\{\text{players}\},
$$

such that

$$
\boxed{
W_h=
\left\{
 d:
C(d)\in\mathcal C_h
\;\text{and}\;
(n,\operatorname{owner}_d(n))\in E_h
\text{ for every card }n
\right\}.
}
$$

Here $\operatorname{owner}_d(n)$ means the **initial** owner of card $n$.

Thus all uncertainty about the initial deal consists of only two kinds:

1. which category-count matrices remain possible;
2. which player could initially have owned each named card.

Transfers do not alter the initial deal and are stored separately as public bookkeeping.

---

## 3. Typed slots and symmetry

For a particular count matrix $C$, the value $c_{pc}$ creates $c_{pc}$ anonymous slots of type

$$
(\text{player }p,\text{ category }c).
$$

For example, if Peter initially has two Flowers, his configuration contains two Peter–Flower slots.

Slots having the same player and category are interchangeable. They always have identical compatibility with card names.

Consequently, the state never needs to distinguish between "Peter's first Flower slot" and "Peter's second Flower slot."

The relation $E_h$, together with a count matrix, induces a bipartite graph between card names and these typed slots.

---

## 4. Base case

Before the game begins, every legal labelled deal determines exactly one count matrix.

For a fixed count matrix $C$, the four distinct cards of category $c$ can be distributed among the players in

$$
\frac{4!}
{c_{1c}!c_{2c}!c_{3c}!}
$$

ways.

Therefore $C$ represents

$$
N(C)=
\prod_{c=A,B,C}
\frac{4!}
{c_{1c}!c_{2c}!c_{3c}!}
$$

labelled deals.

Summing over all count matrices with row sums 4, column sums 4, and no entry equal to 4 gives

$$
34\,032.
$$

Initially every card name is compatible with every player having a slot of the corresponding category.

Hence the invariant holds before play begins.

---

## 5. Public transfers

Every ordinary transfer occurs only after a player asks for a **specific named card in a specific category**, for example:

> "Do you have the Rose from Flowers?"

Therefore every transferred card has a publicly known identity, category, source, and destination.

For player $p$ and category $c$, define the publicly known net transfer offset

$$
\Delta_{pc}
=
\text{cards of category }c\text{ received by }p
-
\text{cards of category }c\text{ given away by }p.
$$

For any candidate initial count matrix,

$$
\boxed{
N_c(p)=c_{pc}+\Delta_{pc}
}
$$

is therefore the player's current number of cards in that category.

The offset is determined entirely by public history and is the same for every surviving possible deal.

---

## 6. Legal request

Suppose Peter asks Quinty for A1.

The rules require that:

1. Peter does not currently possess A1;
2. Peter currently possesses at least one other A-card.

Because condition 1 already excludes A1 from Peter's hand, condition 2 is equivalent to

$$
N_A(P)\ge1.
$$

Using the public transfer offset,

$$
c_{PA}+\Delta_{PA}\ge1.
$$

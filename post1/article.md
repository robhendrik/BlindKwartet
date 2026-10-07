# A Card Game With Cards That Don't Exist (Yet)

*A blind version of the children's game kwartet has 34,032 possible worlds. Keeping track of them leads to a marriage theorem from 1935.*

![Feature image: a hand of cards, one named Electron, three still blank](./figures/feature_image.png)
*Feature image: four cards, one of which has just received its name.*

<!-- Working title and subtitle, not final. Draft status: sections 1 and 2 are Rob's text with typos and grammar fixed; section 3 is a Claude draft for Rob to edit. Running example is physics (elementary particles, electron). The ordinary-kwartet example in paragraph 2 (Archimedes, Greek mathematicians) is a proposal. -->

## Kwartet Without Cards Always Ends in Confusion

Imagine a card game in which no card exists. Not only does no one hold a physical card, but also what is actually on the virtual cards we play with is not yet defined. The cards are made up as you play. The rule is that you are not allowed to make a move that is inconsistent with what happened earlier in the game. A friend proposed this game when we were travelling with some fellow students to a physics conference in the mid-1990s. It was fun, but it always ended in confusion: after a few rounds it became almost impossible to track the history and determine what was still a legal move.

The game is based on the Dutch children's game Kwartet, which is very similar to Go Fish. Players assemble the four cards of a category by asking other players for them. Once you have a complete category you say "Kwartet" and lay down the cards. When you ask for a card you have to be specific ("Can you give me Archimedes from the Greek mathematicians?"). If the other player has the card, it is handed over and you can ask again. If not, it is their turn. You may only ask for a card from a category in which you already hold a card, and never for a card you hold yourself.

In our variant we only fixed how many cards were in the game, how many each player held initially, and the fact that nobody had a kwartet from the start. Then the first question ("Can you give me the electron from the elementary particles?") defined a category (the elementary particles) and one member of that category (the electron). But the question also told us that the first player held at least one other card from the elementary particles, but not the electron. The second player could answer yes or no. Depending on the answer, the card was virtually handed over, or the turn moved to the second player. After a few questions multiple categories were defined, with partially identified members, and a list of constraints on the players' hands emerged. This is where we got lost. Is there a way to manage this bookkeeping?

## Give the Blank Cards Secret Labels

We can keep track of the game by giving each virtual card initially a label. Call the three categories A, B and C, and the cards A1 to A4, B1 to B4 and C1 to C4 (you could imagine that a printer had labelled the deck before the game). We then agree that the first category mentioned is category A, and that the first card in any category gets the label 1. In this situation the names the players invent ("Elementary particles", "Electron") are only entries in a notebook that matches the labels on the cards as the game evolves.

With these labels, the question "what is still possible?" becomes a question we can answer by assessing whether the game state is consistent with a valid initial state. We can take each possible initial state as a world: one complete deal of the twelve labelled cards: who holds which card at the start. With three players holding four cards each, there are 12! / (4!)³ = 34,650 ways to deal. In 618 of them somebody starts with a complete category, which the rules exclude, so 34,032 worlds remain. That is our multiverse: every deal consistent with the rules before the first question is asked. In each world the game then evolves as the players ask and answer questions, and as cards change owner.

Now the referee has a simple job. Give every world one bit, switched on. Every question, answer, transfer and announcement switches off the worlds that contradict it. As long as at least one bit is still on, the game so far is legal. If the last bit goes off, someone made an impossible move.

Note what this is not. There is no true deal hidden somewhere that the players are slowly discovering. When both answers to a question are consistent with the history, the player who answers chooses, and the multiverse shrinks because of that choice, not because anyone found something out. The "reality" that emerges after all questions are asked is a reality that did not exist before. The game is not a deduction puzzle, it is a story that must stay consistent.

This referee is exact and easy to explain. It maintains a full bookkeeping. On the other hand, it is also wasteful. With three players, keeping track of the multiverse requires 34,032 bits. With four players and four categories of four, the same recipe gives 62,513,568 worlds, about 7.8 megabytes of bits for a single state of the game. And most of these worlds differ only in names that nobody has invented yet.

![Figure 1: the state of the game as one bit per world, with the notebook and the history of questions](./figures/figure1_state_as_bits.png)
*Figure 1. The game after two questions: one bit per world, with the notebook and the history beside it.*

## Why Distinguish Cards That Are Still Identical?

Suppose Peter holds cards that did not get any label yet. Why keep separate worlds for two cards whose only difference is a name that does not exist yet? If we swap their labels, we get a different world among the 34,032. But nothing in the game, now or later, can tell the two apart: we have swapped two cards that are both still undefined. The bookkeeping remembers a difference that is not there.

So, can we exploit this? For each player and each category, we only record how many cards that player started with. A hand then has one of three shapes: three cards of one category and one of another (3-1-0), two and two (2-2-0), or two, one and one (2-1-1). The three players together form a 3×3 table of counts, in which every row and column adds up to four and no entry is four. There are 87 such tables, against 34,032 worlds. A table counts cards, it does not name them, which is why the count is significantly reduced.

Names are still relevant, and they are tracked separately. When a card is asked for, it gets a name and a row in a second, small table, the naming matrix, that says which players could have held it at the start.

Figure 2 shows the game of Figure 1 in this form. After Peter's question about the electron (answered no) and Quinty's question about Newton, 42 of the 87 tables are still possible. The naming matrix says that the electron started with Robin, and that Newton did not start with Quinty. Together they describe exactly the same 4,846 worlds as Figure 1.

![Figure 2: the same game state as 87 bits for the count tables plus a naming matrix](./figures/figure2_compressed_state.png)
*Figure 2. The game of Figure 1, compressed: one bit for each of the 87 count tables, plus a naming matrix.*

The saving is large. Instead of 34,032 bits, about 4 kilobytes, the three-player game needs 87 bits and a handful of named cards, roughly a dozen bytes. For four players and four categories the count tables number 8,515, about a kilobyte, against 7.8 megabytes of worlds.

But there is a caveat... Look at the naming matrix. In the multiverse a fifth name in a category of four is noticed at once, because no world survives, and as long as we do not create too many categories or cards in a category there is always room to add a newly mentioned label. In the compressed state we have undefined cards in the game that are yet to receive a category and a label. It is not always the case that we can fit the not yet defined labels on the open cards. It could be that we create an unresolvable puzzle in one round, but only find out a few rounds later.
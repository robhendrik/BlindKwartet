# A Card Game With Cards That Don't Exist (Yet)

*A blind version of the children's game kwartet has 34,032 possible worlds. Keeping track of them leads to a marriage theorem from 1935.*

![Feature image: a hand of cards, one named Electron, three still blank](./figures/feature_image.png)
*Feature image: four cards, one of which has just received its name.*

## Kwartet Without Cards Always Ends in Confusion

Imagine a card game in which no card exists. Not only does no one hold a physical card, but also what is actually on the virtual cards we play with is not yet defined. The cards are made up as you play. The rule is that you are not allowed to make a move that is inconsistent with what happened earlier in the game.

I got to know this game when a friend proposed it while we were travelling with some fellow students to a physics conference in the mid-1990s. It was fun, but it always ended in confusion: after a few rounds it became almost impossible to track the history and determine what was still a legal move.

The game is based on the Dutch children's game Kwartet, which is very similar to Go Fish. Players assemble the four cards of a category by asking other players for them. Once you have a complete category you say "Kwartet" and lay down the cards. When you ask for a card you have to be specific ("Can you give me Archimedes from the Greek mathematicians?"). If the other player has the card, it is handed over and you can ask again. If not, it is their turn. You may only ask for a card from a category in which you already hold a card, and never for a card you hold yourself.

In our variant we only fixed how many cards were in the game, how many each player held initially, and the fact that nobody had a kwartet from the start. Then the first question ("Can you give me the electron from the elementary particles?") defined a category (the elementary particles) and one member of that category (the electron). But the question also told us that the first player held at least one other card from the elementary particles, but not the electron. The second player could answer yes or no. Depending on the answer, the card was virtually handed over, or the turn moved to the second player. After a few questions multiple categories were defined, with partially identified members, and a list of constraints on the players' hands emerged. This is where we got lost. 

To add to the confusion, we could never resist complicating the categories: if someone defined Newton as a physicist, someone else would define a Newton as a unit. But aside from that, is there a way to efficiently manage this bookkeeping and discover whether a move is still legal, given what happened before?

## Give the Blank Cards Secret Labels

We can keep track of the game by giving each virtual card initially a label. Call the three categories A, B and C, and the cards A1 to A4, B1 to B4 and C1 to C4 (you could imagine that a printer had labelled the deck before the game). We then agree that the first category mentioned is category A, and that the first card in any category gets the label 1. In this situation the names the players invent ("Elementary particles", "Electron") are only entries in a notebook that matches the labels on the cards as the game evolves.

With these labels, the question "what is still possible?" becomes a question we can answer by assessing whether the game state is consistent with a valid initial state. We can take each possible initial state as a world: one complete deal of the twelve labelled cards: who holds which card at the start. With three players holding four cards each, there are 12! / (4!)³ = 34,650 ways to deal. In 618 of them somebody starts with a complete category, which the rules exclude, so 34,032 worlds remain. That is our multiverse: every deal consistent with the rules before the first question is asked. In each world the game then evolves as the players ask and answer questions, and as cards change owner.

To referee the game we need one bit per world, all on at the start. Each question, answer, transfer or announcement switches off the worlds it contradicts. As long as one bit is left, the game is legal. The moment the last one goes off, somebody made an impossible move.

Suppose both answers to a question are consistent with the history. The player who answers chooses, and the multiverse shrinks because of that choice, not because anyone found something out. There is no true deal hidden somewhere that the players are slowly discovering. The "reality" that emerges is one that did not exist before: the game is a story that must stay consistent, not a deduction puzzle.

The referee is exact, but it keeps one bit for every world. For three players that is 34,032 bits. For four players and four categories of four it is 62,513,568, about 7.8 megabytes for a single state of the game. Most of these worlds differ only in names that nobody has invented yet.

![Figure 1: the state of the game as one bit per world, with the notebook and the history of questions](./figures/figure1_state_as_bits.png)
*Figure 1. The game after two questions: one bit per world, with the notebook and the history beside it.*

## Why Distinguish Cards That Are Still Identical?

Suppose Peter and Quinty each hold a card that did not get any label yet. If we swap the hidden labels of these two cards, we get a different world among the 34,032, but nothing in the game so far can tell the two apart. Both cards are still undefined, so the multiverse keeps two worlds apart for a difference that does not exist yet.

For each player and each category we only record how many cards that player started with. A hand then has one of three shapes: three cards of one category and one of another (3-1-0), two and two (2-2-0), or two, one and one (2-1-1). The three players together form a 3×3 table of counts, in which every row and column adds up to four and no entry is four. There are 87 such tables, against 34,032 worlds. A table counts cards without labelling them, so many different worlds share the same table.

The counts say nothing about names, so those are tracked separately. When a card is asked for, it gets a name and a row in a second, small table: the naming matrix. For each named card it lists the players who could have held it at the start.

Figure 2 shows the game of Figure 1 in this form. After Peter's question about the electron (answered No) and Quinty's question about Newton, 42 of the 87 tables are still possible. The naming matrix has two rows. The electron started with Robin, because Peter asked for it and Quinty refused. Newton did not start with Quinty, because Quinty asked for it. Together they describe exactly the same 4,846 worlds as Figure 1.

![Figure 2: the same game state as 87 bits for the count tables plus a naming matrix](./figures/figure2_compressed_state.png)
*Figure 2. The game of Figure 1, compressed: one bit for each of the 87 count tables, plus a naming matrix. Each of the 42 lit tables has at least one world left.*

Instead of 34,032 bits, about 4 kilobytes, the three-player game now needs 87 bits for the count tables and a few rows for the named cards: roughly fifteen bytes in total. With four players and four categories there are 8,515 count tables, so about a kilobyte, against 7.8 megabytes of worlds.

But there is a caveat. In the multiverse a fifth name in a category of four is noticed at once, because no world survives. In the compressed state there are undefined cards that have yet to receive a category and a label, and it is not always possible to fit the names we have invented onto those open cards. We could create an unresolvable puzzle in one round, and only find out a few rounds later.

## Locally Possible, Globally Impossible

So, what is the challenge with the naming matrix? It captures the known names and the possible cards these can apply to. As opposed to the multiverse model, we do not assign a card name immediately to a blank card; we instead keep track of which positions can and cannot take this name.

As an example, we continue the game of Figure 1, with only No answers.

1. Peter asks Quinty for the Electron from Elementary Particles. Quinty says No. We now know that the Electron is one of the cards in Robin's hand. (9,032 worlds are left.)
2. Quinty asks Peter for Newton from Physicists. Peter says No. (Now Newton is also one of the cards in Robin's hand. 2,262 worlds are left.)
3. Peter asks Quinty for the muon. No. (418 worlds.)
4. Quinty asks Peter for the photon. No. (No world is left.)

Each question seemed reasonable, and the notebook looks fine. Thirty-six count tables still satisfy what the questions require, and each of the four named cards still has a possible owner. But the final No made the whole history impossible. The electron, the muon and the photon can only be Robin's, since in each case one of Peter and Quinty asked and the other refused. Yet Peter and Quinty both asked for a particle, so each of them holds at least one. That makes five elementary particles in a category of four. In the language of the tables: three names, and at most two places for them at Robin. Figure 3 shows the clash.

![Figure 3: three names that can only be Robin's, and the two particle places Robin has left](./figures/figure3_names_and_places.png)
*Figure 3. Every name still has somewhere to go, but together they do not fit.*

This example is easy to see because everything happens in one category and with one player. With more categories and more cards, names and constraints are interleaved, and an unresolvable state can go unnoticed until much later, or even until the end. Only when we compare all names with all places together does the clash show.

> Every name has somewhere to go. The question is whether they all fit at once.

It turns out that this is a problem mathematicians solved almost a century ago.

## The Question Is a Marriage Problem in Disguise

Can all the names we have invented be placed, one each, in the places that remain? It has a name, and a long history.

Imagine a matchmaker with a group of people. Each person has a list of acceptable partners, and no two people can share a partner. Can everyone be matched at the same time? Our names are the people, our places are the partners, and the list of a name is the set of places where it is still allowed to sit.

The matchmaker can fail in two ways. Someone's list may be empty, which is easy to see. Or a group may be too crowded: three people whose lists contain only the same two partners cannot all be matched, however long the other lists are. That is exactly what happened in Figure 3. The electron, the muon and the photon can only go to Robin, who has two places.

> Checking whether a blind game is still possible is a marriage problem.

In 1935 the mathematician Philip Hall proved that crowded groups are the only thing that can go wrong [4]. If every group of k people has, between them, at least k acceptable partners, then everyone can be matched. This is Hall's marriage theorem (Hall himself wrote about "representatives of subsets"; the marriage wording came later [6]). The link between blind kwartet and this theorem was made in an article in the Dutch magazine Pythagoras [1]. There is a recent paper on Hall’s theorem [5] which gives a recent overview.

The naming matrix tells us, for each name, which players may hold it, and a count table tells us how many places each player has in each category (a count of two means two interchangeable places). For one table we ask whether all names can be placed, category by category. Names that have not been invented yet simply take whatever places are left. If at least one surviving table passes, the game is still possible. If every table fails, it is not. In Figure 3 every table fails: the one shown is the most generous, and the others leave Robin even fewer places.

Hall's condition seems to require checking every group of names, but efficient matching algorithms decide it quickly. They answer a yes-or-no question: does a placement exist? How many there are is a much harder problem. The multiverse kept track of every placement, one bit per world, but to referee the game we only need to know that one exists.

But did the compression, from 34,032 worlds to a few tables and one matrix, throw something away? Could the notebook say "possible" where the multiverse says "impossible", or the other way round?

## Nothing Is Lost by Not Remembering the Worlds

The answer is no. Everything that is said in the game is of one of two kinds. It tells us something about how many cards of a category a player started with, or something about who could have started with a named card. It never mixes the two in one "either-or".

Suppose Peter asks Quinty for the muon. This tells us two things: Peter holds another elementary particle (a statement about counts), and Peter does not hold the muon (a statement about owners). The two facts are joined by "and", never by "or". A Yes works the same way. A named card moves from one player to another, and everybody sees it, so the notebook shifts a known amount in the counts and records where the card came from. A statement such as "either Peter holds three particles or Quinty holds the muon" would tie counts and owners together and break the scheme, but the rules of the game never produce one.

A world survives exactly when its count table is still allowed and every named card sits with a player who could have held it. The two parts of the notebook can be updated independently, but they have to agree, and Hall's theorem checks whether they do. All the rest is public bookkeeping: who gave what to whom, and whose turn it is.

Announcing a quartet keeps only the worlds in which the player holds all four cards of that category, named or not. Continuing without announcing keeps only the worlds in which the player does not. Both are conditions on the counts and on the named cards.

<!-- TODO (Rob): add the result of the side-by-side test here (in particular for Yes answers, quartets and silence). -->

That is a small notebook. Up to 87 bits for the count tables, at most 36 for the naming matrix (twelve cards, three players), plus the transfers and the turn: roughly 150 bits, instead of 34,032.

We started by giving every card a hidden identity, and keeping track of all 34,032 ways those identities might have been distributed. We end with a notebook in which a card that has no name yet stays blank. That is allowed as long as Hall's theorem guarantees that we could fill the blanks in if we wanted to.


## We Can Tell Whether a Move Is Legal. Which Move Is Best?

We now have a referee that can say whether the story so far is possible, and it needs only a small notebook and a matching check. This check can also help us choose the best answer to a question. When someone is asked for a card, we can try both answers. If only one of them leaves a possible game, the answer is forced. If both do, the answerer has a real choice, and that is where strategy begins: a good player chooses the answer that keeps their own hopes alive and the others' hopes small.

So legality was only the first question. The next one is still open: is there a good way to play this game? Because we can now evaluate any state quickly, we can let a computer look ahead, question by question and answer by answer. That is where the next post begins.

## Origins
As stated in the introduction, I encountered this game in the 1990s. When writing this article I came across ‘Quantum Go Fish’, a very similar game that was apparently played in the math community at Berkeley [2, 3]. I do not know whether it was invented once or multiple times, but the game seems to have been around for a while.

## References and Further Reading

The game

1. Jos Brakenhoff and Arjen Stolk (edited by Jeanine Daems), "Blind Kwartetten", Pythagoras 57-3, February 2018, p. 6 (in Dutch). [pyth.eu/blind-kwartetten](https://pyth.eu/blind-kwartetten). 
2. Ben Orlin, "[Quantum Go Fish: A Game of Mysterious Fingers](https://mathwithbaddrawings.com/wp-content/uploads/2026/03/1cf84-game-35-quantum-go-fish.pdf)", chapter "Game 35" (hosted on the Math with Bad Drawings site).
3. "[How to Play Quantum Go Fish](https://stacky.net/wiki/index.php?title=Quantum_Go_Fish)"

The mathematics

4. Philip Hall, "[On representatives of subsets](https://londmathsoc.onlinelibrary.wiley.com/doi/epdf/10.1112/jlms/s1-10.37.26)", Journal of the London Mathematical Society 10 (1935), 26-30.
5. Peter J. Cameron, "Hall's marriage theorem", [arXiv:2503.23159](https://arxiv.org/abs/2503.23159), March 2025. 
6. Paul Halmos and Herbert Vaughan, "The marriage problem", American Journal of Mathematics, 1950.   
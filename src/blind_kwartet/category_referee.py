"""Referee for a single Blind Kwartet category.

A category contains four canonically named cards A1..A4.
Each possible world stores both the initial ownership and the
current ownership after public transfers.
"""

from dataclasses import dataclass
from itertools import product


N_PLAYERS = 3
N_CARDS = 4

OwnerTuple = tuple[int, int, int, int]


@dataclass(frozen=True)
class CategoryWorld:
    """One possible world for a single category.

    Each tuple position corresponds to a card:

        index 0 -> A1
        index 1 -> A2
        index 2 -> A3
        index 3 -> A4

    The value is the player owning that card.
    """

    initial: OwnerTuple
    current: OwnerTuple


@dataclass(frozen=True)
class Question:
    """A question about one card."""

    asker: int
    target: int
    card: int


@dataclass(frozen=True)
class Answer:
    """Answer to the immediately preceding question."""

    yes: bool


def generate_initial_worlds() -> list[CategoryWorld]:
    """Generate all legal initial worlds for one category.

    There are 3^4 = 81 assignments of four cards to three players.
    We exclude the three cases where one player starts with the
    complete quartet.

    Returns:
        The 78 legal initial worlds.
    """
    worlds = []

    for owners in product(range(1, N_PLAYERS + 1), repeat=N_CARDS):
        if len(set(owners)) == 1:
            # One player already owns the complete quartet.
            continue

        owners = tuple(owners)

        worlds.append(
            CategoryWorld(
                initial=owners,
                current=owners,
            )
        )

    return worlds


def apply_question(
    worlds: list[CategoryWorld],
    question: Question,
) -> list[CategoryWorld]:
    """Filter worlds in which a question is legal.

    To ask for card Ak:

    - asker and target must be different players;
    - the asker must currently own at least one card in this category;
    - the asker must not currently own the requested card.

    Asking a question does not itself transfer a card.
    """
    card_index = question.card - 1
    surviving = []

    for world in worlds:
        if question.asker == question.target:
            continue

        if question.asker not in world.current:
            continue

        if world.current[card_index] == question.asker:
            continue

        surviving.append(world)

    return surviving


def apply_answer(
    worlds: list[CategoryWorld],
    question: Question,
    answer: Answer,
) -> list[CategoryWorld]:
    """Filter worlds according to an answer and perform a transfer.

    YES means that the target currently owns the requested card.
    The card is then transferred to the asker.

    NO means that the target does not currently own the card.
    """
    card_index = question.card - 1
    surviving = []

    for world in worlds:
        owner = world.current[card_index]

        if answer.yes:
            if owner != question.target:
                continue

            current = list(world.current)
            current[card_index] = question.asker

            surviving.append(
                CategoryWorld(
                    initial=world.initial,
                    current=tuple(current),
                )
            )

        else:
            if owner == question.target:
                continue

            surviving.append(world)

    return surviving


def format_hand(world: CategoryWorld, initial: bool = False) -> str:
    """Return a readable hand representation for debugging."""
    owners = world.initial if initial else world.current

    hands = []

    for player in range(1, N_PLAYERS + 1):
        cards = [
            f"A{card + 1}"
            for card, owner in enumerate(owners)
            if owner == player
        ]

        hands.append(
            f"P{player}={{{', '.join(cards)}}}"
        )

    return "  ".join(hands)


def run_transcript(
    transcript: list[Question | Answer],
    verbose: bool = True,
) -> list[CategoryWorld]:
    """Replay a transcript over all possible initial worlds."""

    worlds = generate_initial_worlds()
    pending_question = None

    if verbose:
        print(f"Initial worlds: {len(worlds)}")
        print()

    for step, event in enumerate(transcript, start=1):
        before = len(worlds)

        if isinstance(event, Question):
            if pending_question is not None:
                raise ValueError(
                    "New question encountered before previous question "
                    "was answered."
                )

            pending_question = event
            worlds = apply_question(worlds, event)

            description = (
                f"P{event.asker} asks P{event.target} "
                f"for A{event.card}"
            )

        elif isinstance(event, Answer):
            if pending_question is None:
                raise ValueError(
                    "Answer encountered without a pending question."
                )

            worlds = apply_answer(
                worlds,
                pending_question,
                event,
            )

            description = "YES" if event.yes else "NO"
            pending_question = None

        else:
            raise TypeError(f"Unknown transcript event: {event!r}")

        if verbose:
            removed = before - len(worlds)
            percentage = 100 * removed / before if before else 0

            print(f"{step:2}. {description}")
            print(
                f"    {before:2} -> {len(worlds):2} worlds "
                f"(-{removed}, {percentage:.1f}%)"
            )

        if not worlds:
            if verbose:
                print()
                print("Transcript is inconsistent.")
            return []

    if verbose:
        print()
        print(f"{len(worlds)} possible worlds remain.")

        if len(worlds) <= 10:
            print()

            for world in worlds:
                print("initial:", format_hand(world, initial=True))
                print("current:", format_hand(world))
                print()

    return worlds
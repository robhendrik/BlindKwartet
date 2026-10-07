"""Brute-force referee for Blind Quartets / Quantum Happy Families.

Small reference game:
    - 3 players: P1, P2, P3
    - 3 families: A, B, C
    - 4 cards per family: A1 ... C4
    - 4 cards per player

The fundamental hidden state is the INITIAL deal.

For every candidate initial deal, the complete transcript is replayed.
Cards may move between players during the replay, but the candidate
initial deal itself never changes.

After each event, candidate initial deals that cannot reproduce the
observed game history are eliminated.

The resulting set of surviving initial-deal IDs is the information state.
"""

from dataclasses import dataclass
from itertools import combinations


# ---------------------------------------------------------------------------
# Game definition
# ---------------------------------------------------------------------------

PLAYERS = (0, 1, 2)
PLAYER_NAMES = ("P1", "P2", "P3")

FAMILIES = ("A", "B", "C")
CARDS_PER_FAMILY = 4
HAND_SIZE = 4

CARDS = tuple(
    f"{family}{number}"
    for family in FAMILIES
    for number in range(1, CARDS_PER_FAMILY + 1)
)

CARD_INDEX = {card: index for index, card in enumerate(CARDS)}


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Question:
    """A player asks another player for a specific card."""

    asker: int
    target: int
    card: str


@dataclass(frozen=True)
class Answer:
    """Answer to the immediately preceding question."""

    value: bool  # True = YES, False = NO


Event = Question | Answer


# ---------------------------------------------------------------------------
# Initial worlds
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class InitialWorld:
    """One possible initial distribution of all cards."""

    world_id: int

    # owner_by_card[i] is the initial owner of CARDS[i].
    owner_by_card: tuple[int, ...]


def contains_complete_family(hand: set[str]) -> bool:
    """Return whether a hand contains an entire family."""

    for family in FAMILIES:
        quartet = {
            f"{family}{number}"
            for number in range(1, CARDS_PER_FAMILY + 1)
        }

        if quartet <= hand:
            return True

    return False


def generate_initial_worlds(
    exclude_initial_quartets: bool = True,
) -> list[InitialWorld]:
    """Enumerate all possible initial deals."""

    worlds = []
    all_cards = set(CARDS)

    world_id = 0

    for p1_tuple in combinations(CARDS, HAND_SIZE):
        p1 = set(p1_tuple)
        remaining = all_cards - p1

        for p2_tuple in combinations(remaining, HAND_SIZE):
            p2 = set(p2_tuple)
            p3 = remaining - p2

            hands = (p1, p2, p3)

            if exclude_initial_quartets:
                if any(contains_complete_family(hand) for hand in hands):
                    continue

            owner_by_card = tuple(
                next(
                    player
                    for player, hand in enumerate(hands)
                    if card in hand
                )
                for card in CARDS
            )

            worlds.append(
                InitialWorld(
                    world_id=world_id,
                    owner_by_card=owner_by_card,
                )
            )

            world_id += 1

    return worlds


# ---------------------------------------------------------------------------
# Replay state
# ---------------------------------------------------------------------------

@dataclass
class ReplayState:
    """Current physical card locations while replaying one initial world."""

    current_owner: list[int]


def create_replay_state(world: InitialWorld) -> ReplayState:
    """Create the starting physical state for a candidate initial world."""

    return ReplayState(
        current_owner=list(world.owner_by_card)
    )


def owner_of(state: ReplayState, card: str) -> int:
    """Return the current owner of a card."""

    return state.current_owner[CARD_INDEX[card]]


def family_of(card: str) -> str:
    """Return the family label of a card."""

    return card[0]


def player_has_family_card(
    state: ReplayState,
    player: int,
    family: str,
) -> bool:
    """Return whether player currently owns a card from family."""

    return any(
        owner_of(state, card) == player
        for card in CARDS
        if family_of(card) == family
    )


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------

def question_is_legal(
    state: ReplayState,
    question: Question,
) -> bool:
    """Check whether a question is legal in this candidate world."""

    if question.asker == question.target:
        return False

    if question.card not in CARDS:
        return False

    family = family_of(question.card)

    # To ask for a card from a family, the asker must currently
    # possess at least one card from that family.
    if not player_has_family_card(
        state,
        question.asker,
        family,
    ):
        return False

    # A player may ask for another card in a family they hold, but not for a
    # card they already currently own.
    if owner_of(state, question.card) == question.asker:
        return False

    return True


def answer_is_consistent(
    state: ReplayState,
    question: Question,
    answer: Answer,
) -> bool:
    """Check whether an answer matches the current physical state."""

    target_has_card = (
        owner_of(state, question.card)
        == question.target
    )

    return target_has_card == answer.value


def apply_transfer(
    state: ReplayState,
    question: Question,
) -> None:
    """Transfer the requested card after a YES answer."""

    state.current_owner[CARD_INDEX[question.card]] = question.asker


# ---------------------------------------------------------------------------
# Replay one candidate initial world
# ---------------------------------------------------------------------------

def world_survives_prefix(
    world: InitialWorld,
    events: list[Event],
) -> bool:
    """Return whether one initial world can reproduce an event sequence."""

    state = create_replay_state(world)

    pending_question = None

    for event in events:

        if isinstance(event, Question):

            if pending_question is not None:
                raise ValueError(
                    "A new question occurred before the previous "
                    "question was answered."
                )

            if not question_is_legal(state, event):
                return False

            pending_question = event

        elif isinstance(event, Answer):

            if pending_question is None:
                raise ValueError(
                    "Answer encountered without a preceding question."
                )

            if not answer_is_consistent(
                state,
                pending_question,
                event,
            ):
                return False

            if event.value:
                apply_transfer(
                    state,
                    pending_question,
                )

            pending_question = None

        else:
            raise TypeError(
                f"Unknown event type: {type(event)}"
            )

    return True


def _current_state_after_prefix(
    world: InitialWorld,
    events: list[Event],
) -> ReplayState:
    """Replay a valid prefix to obtain its current physical ownership."""
    state = create_replay_state(world)
    pending_question = None
    for event in events:
        if isinstance(event, Question):
            pending_question = event
        else:
            if event.value:
                apply_transfer(state, pending_question)
            pending_question = None
    return state


# ---------------------------------------------------------------------------
# Information state
# ---------------------------------------------------------------------------

def information_state(
    worlds: list[InitialWorld],
    events: list[Event],
) -> frozenset[int]:
    """Return IDs of all initial worlds consistent with the transcript."""

    if events and isinstance(events[-1], Question):
        question = events[-1]
        prior_ids = information_state(worlds, events[:-1])
        if not any(
            question_is_legal(
                current := _current_state_after_prefix(world, events[:-1]),
                question,
            )
            and owner_of(current, question.card) == question.target
            for world in worlds
            if world.world_id in prior_ids
        ):
            return frozenset()

    return frozenset(
        world.world_id
        for world in worlds
        if world_survives_prefix(world, events)
    )


# ---------------------------------------------------------------------------
# Transcript analysis
# ---------------------------------------------------------------------------

def describe_event(
    event: Event,
    pending_question: Question | None,
) -> str:
    """Create a human-readable event description."""

    if isinstance(event, Question):
        return (
            f"{PLAYER_NAMES[event.asker]} asks "
            f"{PLAYER_NAMES[event.target]} for {event.card}"
        )

    answer = "YES" if event.value else "NO"

    if pending_question is None:
        return f"answers {answer}"

    return (
        f"{PLAYER_NAMES[pending_question.target]} "
        f"answers {answer}"
    )


def analyse_transcript(
    worlds: list[InitialWorld],
    events: list[Event],
) -> frozenset[int]:
    """Replay a transcript and show the information gained per event."""

    surviving = frozenset(
        world.world_id
        for world in worlds
    )

    print(f"Initial worlds: {len(surviving):,}")
    print()

    prefix = []
    pending_question = None

    for step, event in enumerate(events, start=1):

        before = surviving

        description = describe_event(
            event,
            pending_question,
        )

        prefix.append(event)

        surviving = information_state(
            worlds,
            prefix,
        )

        removed = len(before) - len(surviving)

        if len(before):
            reduction = 100 * removed / len(before)
        else:
            reduction = 0.0

        print(f"{step:2}. {description}")
        print(
            f"    {len(before):,} -> {len(surviving):,} worlds"
            f"   (-{removed:,}, {reduction:.1f}%)"
        )

        if not surviving:
            print()
            print("*** ILLEGAL TRANSCRIPT ***")
            print(
                "No initial deal can reproduce this history."
            )
            return surviving

        if isinstance(event, Question):
            pending_question = event
        else:
            pending_question = None

    print()
    print("Transcript is consistent.")
    print(
        f"{len(surviving):,} possible initial worlds remain."
    )

    return surviving


# ---------------------------------------------------------------------------
# Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    worlds = generate_initial_worlds(
        exclude_initial_quartets=True
    )

    print(f"Generated {len(worlds):,} legal initial worlds.")
    print()

    transcript = [

        Question(
            asker=0,
            target=1,
            card="A1",
        ),
        Answer(False),

        Question(
            asker=0,
            target=2,
            card="A2",
        ),
        Answer(True),

        # A2 has now moved from P3 to P1.

        Question(
            asker=1,
            target=0,
            card="A2",
        ),
        Answer(True),

        # A2 has now moved from P1 to P2.
    ]

    final_state = analyse_transcript(
        worlds,
        transcript,
    )

    # This frozenset is our information-state key/hashable object.
    print()
    print("Information-state hash:")
    print(hash(final_state))

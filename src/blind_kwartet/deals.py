"""The exact labelled initial-deal universe for the default game.

Deal ids are stable: cards and players are enumerated in their canonical
order, and hands are generated in lexicographic combination order.  Players
are zero-based in this module, as they are in :mod:`blind_kwartet.referee`.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

N_PLAYERS = 3
N_CATEGORIES = 3
CARDS_PER_CATEGORY = 4
TOTAL_CARDS = N_CATEGORIES * CARDS_PER_CATEGORY
CARDS = tuple(
    f"{chr(ord('A') + category)}{number}"
    for category in range(N_CATEGORIES)
    for number in range(1, CARDS_PER_CATEGORY + 1)
)
CARD_INDEX = {card: index for index, card in enumerate(CARDS)}
ALL_DEAL_IDS_MASK: int


@dataclass(frozen=True)
class InitialDeal:
    """One legal, fully labelled initial deal."""

    deal_id: int
    owner_by_card: tuple[int, ...]

    def owner(self, card: int | str) -> int:
        index = CARD_INDEX[card] if isinstance(card, str) else card
        return self.owner_by_card[index]


def _has_initial_quartet(owner_by_card: tuple[int, ...], player: int) -> bool:
    return any(
        all(owner_by_card[category * CARDS_PER_CATEGORY + card] == player
            for card in range(CARDS_PER_CATEGORY))
        for category in range(N_CATEGORIES)
    )


def enumerate_initial_deals() -> tuple[InitialDeal, ...]:
    """Enumerate all legal deals, with deterministic ids ``0..34031``."""
    deals: list[InitialDeal] = []
    cards = tuple(range(TOTAL_CARDS))
    hand_size = TOTAL_CARDS // N_PLAYERS

    for first in combinations(cards, hand_size):
        first_set = set(first)
        remaining = tuple(card for card in cards if card not in first_set)
        for second in combinations(remaining, hand_size):
            second_set = set(second)
            hands = (first_set, second_set, set(remaining) - second_set)
            owners = tuple(
                next(player for player, hand in enumerate(hands) if card in hand)
                for card in cards
            )
            if any(_has_initial_quartet(owners, player)
                   for player in range(N_PLAYERS)):
                continue
            deals.append(InitialDeal(len(deals), owners))
    return tuple(deals)


INITIAL_DEALS = enumerate_initial_deals()
if len(INITIAL_DEALS) != 34_032:  # pragma: no cover - import-time invariant
    raise RuntimeError(f"expected 34032 initial deals, got {len(INITIAL_DEALS)}")

ALL_DEAL_IDS_MASK = (1 << len(INITIAL_DEALS)) - 1

# INITIAL_OWNER_MASKS[player][card] has bit deal_id set when that player
# initially owns that card.
INITIAL_OWNER_MASKS = tuple(
    tuple(
        sum(1 << deal.deal_id for deal in INITIAL_DEALS
            if deal.owner_by_card[card] == player)
        for card in range(TOTAL_CARDS)
    )
    for player in range(N_PLAYERS)
)


def deal_ids(bitset: int) -> tuple[int, ...]:
    """Return the set bits in ascending deal-id order."""
    return tuple(index for index in range(len(INITIAL_DEALS))
                 if bitset & (1 << index))


__all__ = [
    "ALL_DEAL_IDS_MASK", "CARDS", "CARD_INDEX", "CARDS_PER_CATEGORY",
    "INITIAL_DEALS", "INITIAL_OWNER_MASKS", "InitialDeal",
    "N_CATEGORIES", "N_PLAYERS", "TOTAL_CARDS", "deal_ids",
    "enumerate_initial_deals",
]

"""Exact global symmetry transforms for the default labelled game.

Permutation convention: every permutation is indexed by an old label and
stores the corresponding new label.  Card-rank permutations are indexed by
the old category, before that category is moved.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from itertools import permutations, product

from ..deals import (
    ALL_DEAL_IDS_MASK,
    CARDS_PER_CATEGORY,
    INITIAL_DEALS,
    N_CATEGORIES,
    N_PLAYERS,
    TOTAL_CARDS,
)
from ..moves import AnswerMove, Move, QuestionMove, QuartetMove
from ..search_state import NO_OVERRIDE, SearchState


def _inverse_permutation(permutation: tuple[int, ...]) -> tuple[int, ...]:
    inverse = [0] * len(permutation)
    for old, new in enumerate(permutation):
        inverse[new] = old
    return tuple(inverse)


@dataclass(frozen=True)
class SymmetryTransform:
    """One global player/category/card relabelling."""

    player_perm: tuple[int, ...]
    category_perm: tuple[int, ...]
    card_perms: tuple[tuple[int, ...], ...]
    _card_map_value: tuple[int, ...] = field(
        init=False, repr=False, compare=False, hash=False
    )

    def __post_init__(self) -> None:
        if tuple(sorted(self.player_perm)) != tuple(range(N_PLAYERS)):
            raise ValueError("player_perm is not a permutation")
        if tuple(sorted(self.category_perm)) != tuple(range(N_CATEGORIES)):
            raise ValueError("category_perm is not a permutation")
        if len(self.card_perms) != N_CATEGORIES:
            raise ValueError("one card permutation is required per category")
        for permutation in self.card_perms:
            if tuple(sorted(permutation)) != tuple(range(CARDS_PER_CATEGORY)):
                raise ValueError("card permutation is not a permutation")
        object.__setattr__(
            self,
            "_card_map_value",
            tuple(
                self.category_perm[old_category] * CARDS_PER_CATEGORY
                + self.card_perms[old_category][old_rank]
                for old_category in range(N_CATEGORIES)
                for old_rank in range(CARDS_PER_CATEGORY)
            ),
        )

    @classmethod
    def identity(cls) -> "SymmetryTransform":
        identity_players = tuple(range(N_PLAYERS))
        identity_categories = tuple(range(N_CATEGORIES))
        identity_cards = (tuple(range(CARDS_PER_CATEGORY)),) * N_CATEGORIES
        return cls(identity_players, identity_categories, identity_cards)

    @classmethod
    def _from_validated(
        cls,
        player_perm: tuple[int, ...],
        category_perm: tuple[int, ...],
        card_perms: tuple[tuple[int, ...], ...],
    ) -> "SymmetryTransform":
        """Construct group members after enumeration has validated inputs."""
        result = object.__new__(cls)
        object.__setattr__(result, "player_perm", player_perm)
        object.__setattr__(result, "category_perm", category_perm)
        object.__setattr__(result, "card_perms", card_perms)
        object.__setattr__(
            result,
            "_card_map_value",
            tuple(
                category_perm[old_category] * CARDS_PER_CATEGORY
                + card_perms[old_category][old_rank]
                for old_category in range(N_CATEGORIES)
                for old_rank in range(CARDS_PER_CATEGORY)
            ),
        )
        return result

    def transform_card(self, card: int) -> int:
        if card not in range(TOTAL_CARDS):
            raise ValueError("invalid card")
        return _card_map(self)[card]

    def transform_state(self, state: SearchState) -> SearchState:
        return transform_state(state, self)

    def transform_deal_id(self, deal_id: int) -> int:
        return transform_deal_id(deal_id, self)

    def transform_move(self, move: Move) -> Move:
        return transform_move(move, self)

    def inverse(self) -> "SymmetryTransform":
        inverse_category = _inverse_permutation(self.category_perm)
        inverse_cards = [tuple()] * N_CATEGORIES
        for new_category, old_category in enumerate(inverse_category):
            inverse_cards[new_category] = _inverse_permutation(
                self.card_perms[old_category]
            )
        return SymmetryTransform(
            _inverse_permutation(self.player_perm),
            inverse_category,
            tuple(inverse_cards),
        )

    def compose(self, after: "SymmetryTransform") -> "SymmetryTransform":
        """Return the transform obtained by applying ``self`` then ``after``."""
        player = tuple(after.player_perm[self.player_perm[old]]
                       for old in range(N_PLAYERS))
        category = tuple(after.category_perm[self.category_perm[old]]
                         for old in range(N_CATEGORIES))
        cards = []
        for old_category in range(N_CATEGORIES):
            middle_category = self.category_perm[old_category]
            cards.append(tuple(
                after.card_perms[middle_category][
                    self.card_perms[old_category][old_rank]
                ]
                for old_rank in range(CARDS_PER_CATEGORY)
            ))
        return SymmetryTransform(player, category, tuple(cards))


_DEAL_ID_BY_OWNERS = {
    deal.owner_by_card: deal.deal_id
    for deal in INITIAL_DEALS
}

# A compact owner encoding avoids allocating a 12-item tuple and a temporary
# list for every sparse deal/transform pair.  Two bits per card are enough for
# the three players.  This is only an implementation cache; deal ids and D's
# dense bitset remain authoritative.
_DEAL_CODE_BY_ID = tuple(
    sum(owner << (2 * card) for card, owner in enumerate(deal.owner_by_card))
    for deal in INITIAL_DEALS
)
_DEAL_ID_BY_CODE = {code: deal_id for deal_id, code in enumerate(_DEAL_CODE_BY_ID)}


def _card_map(transform: SymmetryTransform) -> tuple[int, ...]:
    return transform._card_map_value


@lru_cache(maxsize=16_384)
def transform_deal_id(
    deal_id: int,
    transform: SymmetryTransform,
) -> int:
    """Map one legal initial-deal ID through one global transform."""
    if deal_id not in range(len(INITIAL_DEALS)):
        raise ValueError("invalid deal id")
    old_code = _DEAL_CODE_BY_ID[deal_id]
    new_code = 0
    card_map = _card_map(transform)
    for old_card in range(TOTAL_CARDS):
        old_owner = (old_code >> (2 * old_card)) & 3
        new_code |= transform.player_perm[old_owner] << (2 * card_map[old_card])
    try:
        return _DEAL_ID_BY_CODE[new_code]
    except KeyError as error:  # pragma: no cover - protects the universe invariant
        raise ValueError("transform produced an illegal initial deal") from error


@lru_cache(maxsize=65_536)
def _transform_deal_id_packed(
    deal_id: int,
    transform: SymmetryTransform,
) -> int:
    """Uncached packed hot path used by canonicalization."""
    old_code = _DEAL_CODE_BY_ID[deal_id]
    new_code = 0
    mapped_cards = transform._card_map_value
    for old_card in range(TOTAL_CARDS):
        old_owner = (old_code >> (2 * old_card)) & 3
        new_code |= transform.player_perm[old_owner] << (2 * mapped_cards[old_card])
    return _DEAL_ID_BY_CODE[new_code]


def _transform_bitset(bitset: int, transform: SymmetryTransform) -> int:
    if bitset == ALL_DEAL_IDS_MASK:
        return bitset
    result = 0
    remaining = bitset
    while remaining:
        low_bit = remaining & -remaining
        old_deal_id = low_bit.bit_length() - 1
        result |= 1 << transform_deal_id(old_deal_id, transform)
        remaining ^= low_bit
    return result


def _transform_normalized_state(
    normalized: SearchState,
    transform: SymmetryTransform,
) -> SearchState:
    """Transform a state known by the caller to have normalized T."""
    transformed_overrides = [NO_OVERRIDE] * TOTAL_CARDS
    for old_card, owner in enumerate(normalized.T):
        if owner != NO_OVERRIDE:
            transformed_overrides[transform.transform_card(old_card)] = (
                transform.player_perm[owner]
            )
    # A normalized override remains normalized under a bijective relabelling;
    # avoid rescanning D for every member of the reference group.
    return SearchState(
        possible_initial_deals=_transform_bitset(normalized.D, transform),
        current_owner_override=tuple(transformed_overrides),
        actor=transform.player_perm[normalized.actor],
    )


def transform_state(state: SearchState, transform: SymmetryTransform) -> SearchState:
    """Apply one global transform to D, T, and actor, then normalize T."""
    return _transform_normalized_state(state.normalize_overrides(), transform)


def transform_move(move: Move, transform: SymmetryTransform) -> Move:
    """Transform a typed move; YES/NO are label-independent."""
    if isinstance(move, QuestionMove):
        return QuestionMove(
            target=transform.player_perm[move.target],
            category=transform.category_perm[move.category],
            card=transform.transform_card(move.card),
        )
    if isinstance(move, QuartetMove):
        return QuartetMove(category=transform.category_perm[move.category])
    if isinstance(move, AnswerMove):
        return move
    raise TypeError(f"unsupported move type: {type(move)!r}")


@lru_cache(maxsize=3)
def actor_normalized_transforms(actor: int) -> tuple[SymmetryTransform, ...]:
    """Enumerate exactly the 165,888 transforms sending ``actor`` to zero."""
    if actor not in range(N_PLAYERS):
        raise ValueError("invalid actor")
    player_perms = tuple(
        tuple(0 if old == actor else 1 + remaining.index(old)
              for old in range(N_PLAYERS))
        for remaining in permutations(tuple(old for old in range(N_PLAYERS) if old != actor))
    )
    category_perms = tuple(permutations(range(N_CATEGORIES)))
    card_perms = tuple(permutations(range(CARDS_PER_CATEGORY)))
    transforms = []
    for player_perm, category_perm, cards in product(
        player_perms, category_perms, product(card_perms, repeat=N_CATEGORIES)
    ):
        transforms.append(
            SymmetryTransform._from_validated(player_perm, category_perm, cards)
        )
    return tuple(transforms)


__all__ = [
    "SymmetryTransform",
    "actor_normalized_transforms",
    "transform_deal_id",
    "transform_move",
    "transform_state",
]

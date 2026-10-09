"""Diagnostic Hall/notebook key derived from the authoritative SearchState.

This module deliberately does not replace ``SearchState``.  It projects the
exact ``(D, T, actor)`` state into the representation described in the
article: surviving cross-category count combinations plus per-card naming
constraints and public current-owner information.  The projection is useful
for measuring compression, but the projection is not assumed to be lossless.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from functools import lru_cache

from .deals import (
    CARDS_PER_CATEGORY,
    INITIAL_DEALS,
    INITIAL_OWNER_MASKS,
    N_CATEGORIES,
    N_PLAYERS,
    TOTAL_CARDS,
)
from .search_state import NO_OVERRIDE, SearchState


OwnerMask = int
CardConstraint = tuple[OwnerMask, OwnerMask, int]
CategoryDescriptor = tuple[int, int | None, tuple[CardConstraint, ...]]
CountTable = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class CompressedSearchKey:
    """Exact immutable candidate key for a normalized notebook state.

    ``count_tables`` is the surviving set of complete category count tables.
    Each card constraint is ``(initial-owner-mask, current-owner-mask,
    transfer-owner)``; ``transfer-owner`` is ``-1`` when the current owner is
    still derived from the initial world and otherwise is the public owner.
    The resolved marker and holder are retained because they affect legal
    actions and scoring.
    """

    count_tables: tuple[CountTable, ...]
    categories: tuple[CategoryDescriptor, ...]


def _player_map(actor: int) -> tuple[int, ...]:
    next_player = (actor + 1) % N_PLAYERS
    return tuple(
        0 if player == actor else 1 if player == next_player else 2
        for player in range(N_PLAYERS)
    )


def _map_mask(mask: int, player_map: tuple[int, ...]) -> int:
    result = 0
    for old_player in range(N_PLAYERS):
        if mask & (1 << old_player):
            result |= 1 << player_map[old_player]
    return result


@lru_cache(maxsize=1)
def _deal_count_tables() -> tuple[CountTable, ...]:
    tables = []
    for deal in INITIAL_DEALS:
        categories = []
        for category in range(N_CATEGORIES):
            owners = deal.owner_by_card[
                category * CARDS_PER_CATEGORY:(category + 1) * CARDS_PER_CATEGORY
            ]
            categories.append(tuple(owners.count(player) for player in range(N_PLAYERS)))
        tables.append(tuple(categories))
    return tuple(tables)


@lru_cache(maxsize=1)
def _count_table_masks() -> tuple[tuple[CountTable, int], ...]:
    masks: dict[CountTable, int] = {}
    for deal_id, table in enumerate(_deal_count_tables()):
        masks[table] = masks.get(table, 0) | (1 << deal_id)
    return tuple(masks.items())


def _allowed_masks(state: SearchState) -> tuple[int, ...]:
    return tuple(
        sum(1 << player for player in range(N_PLAYERS)
            if INITIAL_OWNER_MASKS[player][card] & state.D)
        for card in range(TOTAL_CARDS)
    )


def _current_masks(state: SearchState) -> tuple[int, ...]:
    return tuple(
        (1 << state.T[card]) if state.T[card] != NO_OVERRIDE else initial_mask
        for card, initial_mask in enumerate(_allowed_masks(state))
    )


def _count_tables(state: SearchState, player_map: tuple[int, ...]) -> tuple[CountTable, ...]:
    tables = set()
    for source_table, deal_mask in _count_table_masks():
        if not (deal_mask & state.D):
            continue
        transformed = tuple(
            tuple(
                sum(counts[old] for old in range(N_PLAYERS)
                    if player_map[old] == new)
                for new in range(N_PLAYERS)
            )
            for counts in source_table
        )
        tables.add(transformed)
    return tuple(sorted(tables))


def _category_descriptors(
    state: SearchState,
    player_map: tuple[int, ...],
    initial_masks: tuple[int, ...],
    current_masks: tuple[int, ...],
) -> tuple[CategoryDescriptor, ...]:
    descriptors = []
    resolved = state.resolved_categories
    holders = state.quartet_holders()
    for category in range(N_CATEGORIES):
        cards = []
        for offset in range(CARDS_PER_CATEGORY):
            card = category * CARDS_PER_CATEGORY + offset
            transfer = state.T[card]
            transfer = -1 if transfer == NO_OVERRIDE else player_map[transfer]
            cards.append((
                _map_mask(initial_masks[card], player_map),
                _map_mask(current_masks[card], player_map),
                transfer,
            ))
        # Public transfers name their card slots.  Preserve their relative
        # positions so a P2/P3 reflection cannot be hidden by sorting a pair
        # of differently owned named cards.  Cards without a public transfer
        # are still interchangeable when their exact constraints agree.
        if any(card[2] != -1 for card in cards):
            canonical_cards = tuple(cards)
        else:
            canonical_cards = tuple(sorted(cards))
        holder = None if holders[category] is None else player_map[holders[category]]
        descriptors.append((
            int(category in resolved),
            holder,
            canonical_cards,
        ))
    return tuple(descriptors)


def _permute_count_tables(
    count_tables: tuple[CountTable, ...], permutation: tuple[int, ...]
) -> tuple[CountTable, ...]:
    return tuple(sorted(tuple(table[old] for old in permutation) for table in count_tables))


def compressed_search_key(state: SearchState) -> CompressedSearchKey:
    """Build the diagnostic canonical Hall/notebook key.

    Actor normalization is cyclic and deterministic.  Category symmetry uses
    only the six category permutations; card symmetry is handled by sorting
    exact per-card constraint descriptors inside each category.
    """
    normalized = state.normalize_overrides()
    player_map = _player_map(normalized.actor)
    count_tables = _count_tables(normalized, player_map)
    initial_masks = _allowed_masks(normalized)
    current_masks = _current_masks(normalized)
    categories = _category_descriptors(
        normalized, player_map, initial_masks, current_masks
    )
    candidates = []
    for permutation in permutations(range(N_CATEGORIES)):
        candidates.append(CompressedSearchKey(
            count_tables=_permute_count_tables(count_tables, permutation),
            categories=tuple(categories[old] for old in permutation),
        ))
    return min(
        candidates,
        key=lambda candidate: (candidate.count_tables, candidate.categories),
    )


def compressed_projection(state: SearchState) -> dict[str, object]:
    """Return diagnostic details, including Hall-style consistency checks."""
    key = compressed_search_key(state)
    return {
        "key": key,
        "count_table_count": len(key.count_tables),
        "named_or_constrained_cards": sum(
            any(mask != (1 << N_PLAYERS) - 1 for mask in card[:2]) or card[2] != -1
            for category in key.categories
            for card in category[2]
        ),
        "resolved_categories": sum(category[0] for category in key.categories),
        "authoritative_worlds": state.D.bit_count(),
    }


def _capacity_matchable(masks: tuple[int, ...], capacities: tuple[int, ...]) -> bool:
    """Small exact bipartite matching check for one count table/category."""
    remaining = list(capacities)

    def assign(index: int) -> bool:
        if index == len(masks):
            return True
        for owner in range(N_PLAYERS):
            if masks[index] & (1 << owner) and remaining[owner]:
                remaining[owner] -= 1
                if assign(index + 1):
                    return True
                remaining[owner] += 1
        return False

    return assign(0)


def compressed_validation(state: SearchState) -> dict[str, object]:
    """Validate the projected notebook facts against the exact state.

    This validates local Hall/count consistency and public transfer markers.
    It intentionally reports that cross-category world correlation is not
    encoded by the candidate key; callers must not treat this as proof that
    the projection is a lossless replacement for ``D``.
    """
    key = compressed_search_key(state)
    card_masks = tuple(
        category[2] for category in key.categories
    )
    hall_consistent = any(
        all(
            _capacity_matchable(
                tuple(card[0] for card in card_masks[category]),
                table[category],
            )
            for category in range(N_CATEGORIES)
        )
        for table in key.count_tables
    )
    transfer_consistent = all(
        transfer == -1 or current_mask == (1 << transfer)
        for category in card_masks
        for initial_mask, current_mask, transfer in category
    )
    return {
        "candidate_hall_consistent": hall_consistent,
        "transfer_markers_consistent": transfer_consistent,
        "authoritative_worlds_positive": bool(state.D),
        "resolved_categories_represented": True,
        "cross_category_world_correlations_encoded": False,
    }


__all__ = [
    "CompressedSearchKey", "compressed_projection", "compressed_search_key",
    "compressed_validation",
]

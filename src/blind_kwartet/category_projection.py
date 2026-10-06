"""Project the global public search state to one local category bitmap."""

from __future__ import annotations

from .deals import CARDS_PER_CATEGORY, N_CATEGORIES, N_PLAYERS
from .search_state import SearchState
from .single_category_solver import world_bit


def project_category_bitmap(
    state: SearchState,
    category: int,
    active_player_id: int,
) -> int:
    """Return possible current worlds for ``category`` in hero-relative IDs.

    ``SearchState`` remains authoritative: each surviving initial deal is
    projected through ``current_owner``, which applies public transfer
    overrides before the local owners are normalized to P1/P2/P3.
    """
    if not isinstance(state, SearchState):
        raise TypeError("state must be a SearchState")
    if category not in range(N_CATEGORIES):
        raise ValueError("invalid category")
    if active_player_id not in range(N_PLAYERS):
        raise ValueError("invalid active player")

    relative_player = {
        active_player_id: 0,
        (active_player_id + 1) % N_PLAYERS: 1,
        (active_player_id + 2) % N_PLAYERS: 2,
    }
    first_card = category * CARDS_PER_CATEGORY
    bitmap = 0
    for deal_id in state.surviving_deal_ids():
        current_owners = tuple(
            relative_player[state.current_owner(deal_id, first_card + offset)]
            for offset in range(CARDS_PER_CATEGORY)
        )
        bitmap |= world_bit(current_owners)  # type: ignore[arg-type]
    return bitmap


__all__ = ["project_category_bitmap"]

"""Project the global public search state to one local category bitmap."""

from __future__ import annotations

from dataclasses import dataclass
import time

import numpy as np

from .deals import CARDS_PER_CATEGORY, INITIAL_OWNER, N_CATEGORIES, N_PLAYERS
from .search_state import SearchState
from .single_category_solver import world_bit


@dataclass
class ProjectionDiagnostics:
    calls: int = 0
    enumeration_ns: int = 0
    owner_table_ns: int = 0
    override_ns: int = 0
    encoding_ns: int = 0
    accumulation_ns: int = 0


def _validate(state: SearchState, category: int, active_player_id: int) -> None:
    if not isinstance(state, SearchState):
        raise TypeError("state must be a SearchState")
    if category not in range(N_CATEGORIES):
        raise ValueError("invalid category")
    if active_player_id not in range(N_PLAYERS):
        raise ValueError("invalid active player")


def _fast_deal_ids(bitset: int) -> np.ndarray:
    ids: list[int] = []
    while bitset:
        least = bitset & -bitset
        ids.append(least.bit_length() - 1)
        bitset ^= least
    return np.asarray(ids, dtype=np.int64)


def _project_python(state, category, active_player_id, diagnostics):
    relative_player = {
        active_player_id: 0,
        (active_player_id + 1) % N_PLAYERS: 1,
        (active_player_id + 2) % N_PLAYERS: 2,
    }
    first_card = category * CARDS_PER_CATEGORY
    started = time.perf_counter_ns() if diagnostics is not None else 0
    deal_ids = state.surviving_deal_ids()
    if diagnostics is not None:
        diagnostics.enumeration_ns += time.perf_counter_ns() - started
    bitmap = 0
    for deal_id in deal_ids:
        current_owners = tuple(
            relative_player[state.current_owner(deal_id, first_card + offset)]
            for offset in range(CARDS_PER_CATEGORY)
        )
        bitmap |= world_bit(current_owners)  # type: ignore[arg-type]
    return bitmap


def _project_numpy(state, category, active_player_id, diagnostics):
    started = time.perf_counter_ns() if diagnostics is not None else 0
    deal_ids = _fast_deal_ids(state.D)
    if diagnostics is not None:
        diagnostics.enumeration_ns += time.perf_counter_ns() - started
    first_card = category * CARDS_PER_CATEGORY
    cards = np.arange(first_card, first_card + CARDS_PER_CATEGORY, dtype=np.int64)
    started = time.perf_counter_ns() if diagnostics is not None else 0
    owners = INITIAL_OWNER[deal_ids[:, None], cards[None, :]].astype(np.int8, copy=True)
    if diagnostics is not None:
        diagnostics.owner_table_ns += time.perf_counter_ns() - started
    started = time.perf_counter_ns() if diagnostics is not None else 0
    overrides = np.asarray(state.T[first_card:first_card + CARDS_PER_CATEGORY], dtype=np.int8)
    for offset, override in enumerate(overrides):
        if override >= 0:
            owners[:, offset] = override
    if diagnostics is not None:
        diagnostics.override_ns += time.perf_counter_ns() - started
    started = time.perf_counter_ns() if diagnostics is not None else 0
    owners = (owners - active_player_id) % N_PLAYERS
    codes = owners[:, 0] + 3 * owners[:, 1] + 9 * owners[:, 2] + 27 * owners[:, 3]
    if diagnostics is not None:
        diagnostics.encoding_ns += time.perf_counter_ns() - started
    started = time.perf_counter_ns() if diagnostics is not None else 0
    bitmap = 0
    for code in np.unique(codes):
        bitmap |= 1 << int(code)
    if diagnostics is not None:
        diagnostics.accumulation_ns += time.perf_counter_ns() - started
    return bitmap


_NUMBA_PROJECT = None


def _get_numba_project():
    global _NUMBA_PROJECT
    if _NUMBA_PROJECT is not None:
        return _NUMBA_PROJECT
    try:
        from numba import njit
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Numba backend requested but numba is unavailable") from exc

    @njit(cache=False)
    def project_kernel(ids, owner_table, first_card, overrides, active_player):
        low = np.uint64(0)
        high = np.uint64(0)
        for row in range(ids.shape[0]):
            code = 0
            multiplier = 1
            for offset in range(4):
                owner = overrides[offset]
                if owner < 0:
                    owner = owner_table[ids[row], first_card + offset]
                owner = (owner - active_player) % 3
                code += owner * multiplier
                multiplier *= 3
            if code < 64:
                low |= np.uint64(1) << np.uint64(code)
            else:
                high |= np.uint64(1) << np.uint64(code - 64)
        return low, high

    _NUMBA_PROJECT = project_kernel
    return _NUMBA_PROJECT


def _project_numba(state, category, active_player_id, diagnostics):
    started = time.perf_counter_ns() if diagnostics is not None else 0
    deal_ids = _fast_deal_ids(state.D)
    if diagnostics is not None:
        diagnostics.enumeration_ns += time.perf_counter_ns() - started
    overrides = np.asarray(
        state.T[category * CARDS_PER_CATEGORY:(category + 1) * CARDS_PER_CATEGORY],
        dtype=np.int64,
    )
    started = time.perf_counter_ns() if diagnostics is not None else 0
    low, high = _get_numba_project()(
        deal_ids, INITIAL_OWNER, category * CARDS_PER_CATEGORY,
        overrides, active_player_id,
    )
    if diagnostics is not None:
        diagnostics.encoding_ns += time.perf_counter_ns() - started
    return int(low) | (int(high) << 64)


def project_category_bitmap(
    state: SearchState,
    category: int,
    active_player_id: int,
    *,
    backend: str = "python",
    diagnostics: ProjectionDiagnostics | None = None,
) -> int:
    """Return possible current worlds for ``category`` in hero-relative IDs.

    ``SearchState`` remains authoritative: each surviving initial deal is
    projected through ``current_owner``, which applies public transfer
    overrides before the local owners are normalized to P1/P2/P3.
    """
    _validate(state, category, active_player_id)
    if backend not in {"python", "numpy", "numba"}:
        raise ValueError("backend must be 'python', 'numpy', or 'numba'")
    if diagnostics is not None:
        diagnostics.calls += 1
    if backend == "python":
        return _project_python(state, category, active_player_id, diagnostics)
    if backend == "numpy":
        return _project_numpy(state, category, active_player_id, diagnostics)
    return _project_numba(state, category, active_player_id, diagnostics)


__all__ = ["ProjectionDiagnostics", "project_category_bitmap"]

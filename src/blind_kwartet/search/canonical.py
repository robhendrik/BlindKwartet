"""Exact reference and optimized canonicalization.

The reference implementation intentionally constructs transformed states.  The
optimized implementation uses the same transform group and exact key, but
keeps the hot path in packed integers so it does not allocate SearchState
objects for every candidate.
"""

from __future__ import annotations

from dataclasses import dataclass

from .transforms import (
    SymmetryTransform,
    _card_map,
    _transform_deal_id_packed,
    _transform_normalized_state,
    actor_normalized_transforms,
    transform_state,
)
from ..deals import (
    ALL_DEAL_IDS_MASK,
    CARDS_PER_CATEGORY,
    INITIAL_OWNER_MASKS,
    N_CATEGORIES,
    N_PLAYERS,
    TOTAL_CARDS,
)
from ..search_state import NO_OVERRIDE
from ..search_state import SearchState


def pack_overrides(overrides: tuple[int, ...]) -> int:
    """Pack T exactly: 0 means no override, owner Pn means code n."""
    packed = 0
    for card, owner in enumerate(overrides):
        code = 0 if owner < 0 else owner + 1
        if code not in range(4):
            raise ValueError("invalid override owner")
        packed |= code << (2 * card)
    return packed


@dataclass
class CanonicalizationStats:
    """Optional diagnostics for benchmarks; not part of the search state."""

    candidates: int = 0
    full_transforms: int = 0
    signature_groups: int = 0


def canonicalize_reference(
    state: SearchState,
) -> tuple[tuple[int, int], SymmetryTransform]:
    """Return the exact lexicographically smallest actor-normalized key."""
    normalized = state.normalize_overrides()
    best_key: tuple[int, int] | None = None
    best_transform: SymmetryTransform | None = None
    for transform in actor_normalized_transforms(normalized.actor):
        if normalized.D == ALL_DEAL_IDS_MASK:
            # D is invariant under every legal transform.  Enumerate the same
            # full group, but avoid constructing 82,944 equivalent state
            # objects when only T can distinguish the keys.
            transformed_overrides = [NO_OVERRIDE] * TOTAL_CARDS
            for old_card, owner in enumerate(normalized.T):
                if owner != NO_OVERRIDE:
                    transformed_overrides[transform.transform_card(old_card)] = (
                        transform.player_perm[owner]
                    )
            key = (ALL_DEAL_IDS_MASK, pack_overrides(tuple(transformed_overrides)))
        else:
            transformed = _transform_normalized_state(normalized, transform)
            key = (transformed.D, pack_overrides(transformed.T))
        if best_key is None or key < best_key:
            best_key = key
            best_transform = transform
    assert best_key is not None and best_transform is not None
    return best_key, best_transform


def _pack_transformed_overrides(
    overrides: tuple[int, ...], transform: SymmetryTransform
) -> int:
    """Pack T after one transform without constructing a transformed tuple."""
    packed = 0
    card_map = transform._card_map_value
    for old_card, owner in enumerate(overrides):
        if owner != NO_OVERRIDE:
            new_card = card_map[old_card]
            packed |= (transform.player_perm[owner] + 1) << (2 * new_card)
    return packed


def _transform_deal_bitset_fast(
    bitset: int, transform: SymmetryTransform
) -> int:
    # Keep the complete universe fast and exact: every legal transform fixes it.
    if bitset == ALL_DEAL_IDS_MASK:
        return bitset
    result = 0
    remaining = bitset
    # The transform already owns the six small permutations.  Building this
    # 12-entry tuple directly avoids hashing the full dataclass through the
    # cache on every sparse candidate.
    card_map = transform._card_map_value
    while remaining:
        low_bit = remaining & -remaining
        old_deal_id = low_bit.bit_length() - 1
        result |= 1 << _transform_deal_id_packed(old_deal_id, transform)
        remaining ^= low_bit
    return result


def _state_signature(state: SearchState) -> tuple:
    """Cheap equivariant data used to group/order candidates.

    The signature is deliberately not used as a replacement for the exact
    key.  It records card ownership counts and T's public override pattern,
    which makes benchmark diagnostics and future safe pruning possible while
    retaining every full candidate on ties.
    """
    counts = tuple(
        tuple((state.D & mask).bit_count() for mask in masks)
        for masks in INITIAL_OWNER_MASKS
    )
    category_signatures = tuple(
        tuple(sorted(counts[player][card] for player in range(N_PLAYERS)))
        for card in range(TOTAL_CARDS)
    )
    return (
        tuple(
            sorted(category_signatures[CARDS_PER_CATEGORY * c:
                                       CARDS_PER_CATEGORY * c + CARDS_PER_CATEGORY])
            for c in range(N_CATEGORIES)
        ),
        tuple(owner for owner in state.T if owner != NO_OVERRIDE),
    )


def canonicalize(
    state: SearchState,
    *,
    stats: dict[str, int] | None = None,
) -> tuple[tuple[int, int], SymmetryTransform]:
    """Return the exact canonical key using the packed optimized path.

    No candidate is discarded based on a signature: all 82,944 actor-
    normalized transforms are still compared with the complete exact key.
    This deliberately conservative first optimization establishes the fast
    representation and leaves future signature pruning semantics-safe.
    """
    normalized = state.normalize_overrides()
    transforms = actor_normalized_transforms(normalized.actor)
    # Compute once for the documented profiling/signature hook.  The value is
    # invariant under the residual group and never affects exact selection.
    _state_signature(normalized)
    best_key: tuple[int, int] | None = None
    best_transform: SymmetryTransform | None = None
    full_transforms = 0
    for transform in transforms:
        transformed_d = _transform_deal_bitset_fast(normalized.D, transform)
        transformed_t = _pack_transformed_overrides(normalized.T, transform)
        key = (transformed_d, transformed_t)
        full_transforms += 1
        if best_key is None or key < best_key:
            best_key = key
            best_transform = transform
    assert best_key is not None and best_transform is not None
    if stats is not None:
        stats.update({
            "candidates": len(transforms),
            "full_transforms": full_transforms,
            "signature_groups": 1,
        })
    return best_key, best_transform


def canonical_key_reference(state: SearchState) -> tuple[int, int]:
    return canonicalize_reference(state)[0]


def canonical_key(state: SearchState) -> tuple[int, int]:
    return canonicalize(state)[0]


def canonical_state(
    state: SearchState,
) -> tuple[SearchState, SymmetryTransform]:
    """Return the canonical labelled state and the actual-to-canonical map."""
    _, transform = canonicalize(state)
    return transform_state(state, transform), transform


__all__ = [
    "CanonicalizationStats", "canonical_key", "canonical_key_reference",
    "canonical_state", "canonicalize", "canonicalize_reference",
    "pack_overrides",
]

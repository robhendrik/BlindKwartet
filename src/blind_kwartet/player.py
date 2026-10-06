"""Compatibility re-exports for the player interface."""

from .players import (
    Player,
    PlayerView,
    RandomPlayer,
    SingleCategoryTreePlayer,
    TreeDecisionDiagnostic,
)

__all__ = [
    "Player",
    "PlayerView",
    "RandomPlayer",
    "SingleCategoryTreePlayer",
    "TreeDecisionDiagnostic",
]

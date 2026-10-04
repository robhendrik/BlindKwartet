"""Canonical mapping from spoken names to internal labels."""

from __future__ import annotations

import string

from .events import Question, RawQuestion
from .exceptions import IllegalEvent
from .state import GameState


def normalize_name(name: str) -> str:
    """Normalize a spoken/display name for stable lookup."""
    normalized = " ".join(name.strip().split()).casefold()
    if not normalized:
        raise IllegalEvent("Names may not be empty.")
    return normalized


def canonical_category_label(category: int) -> str:
    """Return A, B, C, ... for a canonical category index."""
    if category < len(string.ascii_uppercase):
        return string.ascii_uppercase[category]
    return f"C{category + 1}"


def canonical_card_label(category: int, card: int) -> str:
    """Return labels such as A1, A2, B1, ..."""
    return f"{canonical_category_label(category)}{card + 1}"


class MappingReferee:
    """Owns only the spoken-name -> canonical-label rules."""

    def resolve_category(self, state: GameState, raw_name: str) -> int:
        """Resolve an existing category name or assign the next canonical one."""
        name = normalize_name(raw_name)

        if name in state.naming.category_names:
            return state.naming.category_names[name]

        next_index = len(state.naming.category_names)
        if next_index >= state.config.n_categories:
            raise IllegalEvent(
                f"Cannot introduce category {raw_name!r}: "
                "all canonical categories are already named."
            )

        state.naming.category_names[name] = next_index
        state.naming.card_names.setdefault(next_index, {})
        return next_index

    def resolve_card(
        self,
        state: GameState,
        category: int,
        raw_name: str,
    ) -> int:
        """Resolve or assign a canonical card name within a category."""
        name = normalize_name(raw_name)
        mapping = state.naming.card_names.setdefault(category, {})

        if name in mapping:
            return mapping[name]

        next_index = len(mapping)
        if next_index >= state.config.cards_per_category:
            raise IllegalEvent(
                f"Cannot introduce card {raw_name!r}: "
                "all card labels in this category are already used."
            )

        mapping[name] = next_index
        return next_index

    def resolve_question(
        self,
        state: GameState,
        raw: RawQuestion,
    ) -> Question:
        """Canonicalize a raw human question."""
        category = self.resolve_category(state, raw.category_name)
        card = self.resolve_card(state, category, raw.card_name)

        return Question(
            asker=raw.asker,
            target=raw.target,
            category=category,
            card=card,
        )

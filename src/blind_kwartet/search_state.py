"""Exact Milestone 1 search state and replay adapter.

This module deliberately contains no player strategy or search algorithm.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable

from .deals import (
    ALL_DEAL_IDS_MASK,
    CARD_INDEX,
    CARDS_PER_CATEGORY,
    INITIAL_DEALS,
    N_PLAYERS,
    TOTAL_CARDS,
    deal_ids,
)

NO_OVERRIDE = -1


@dataclass(frozen=True)
class SearchState:
    """The exact public strategic state ``(D, T, actor)``.

    Players and cards are zero-based.  ``current_owner_override`` contains
    ``NO_OVERRIDE`` for cards whose current owner is still read from the
    candidate initial deal.
    """

    possible_initial_deals: int
    current_owner_override: tuple[int, ...]
    actor: int

    def __post_init__(self) -> None:
        if self.possible_initial_deals & ~ALL_DEAL_IDS_MASK:
            raise ValueError("D contains an unknown deal id")
        if len(self.current_owner_override) != TOTAL_CARDS:
            raise ValueError("T must contain one entry per card")
        if any(owner != NO_OVERRIDE and owner not in range(N_PLAYERS)
               for owner in self.current_owner_override):
            raise ValueError("invalid current-owner override")
        if self.actor not in range(N_PLAYERS):
            raise ValueError("invalid actor")

    @classmethod
    def initial(cls, actor: int = 0) -> "SearchState":
        return cls(ALL_DEAL_IDS_MASK, (NO_OVERRIDE,) * TOTAL_CARDS, actor)

    @property
    def D(self) -> int:
        return self.possible_initial_deals

    @property
    def T(self) -> tuple[int, ...]:
        return self.current_owner_override

    def surviving_deal_ids(self) -> tuple[int, ...]:
        return deal_ids(self.possible_initial_deals)

    def current_owner(self, deal_id: int, card: int | str) -> int:
        card_index = CARD_INDEX[card] if isinstance(card, str) else card
<<<<<<< HEAD
=======
        if card_index not in range(TOTAL_CARDS):
            raise ValueError("invalid card")
        if deal_id not in range(len(INITIAL_DEALS)):
            raise ValueError("invalid deal id")
>>>>>>> 4b78765eccd36c34aecb1a0b3ece8cc63c14876e
        override = self.current_owner_override[card_index]
        return (override if override != NO_OVERRIDE
                else INITIAL_DEALS[deal_id].owner_by_card[card_index])

    def current_owners(self, deal_id: int) -> tuple[int, ...]:
        return tuple(self.current_owner(deal_id, card)
                     for card in range(TOTAL_CARDS))

    def _filter(self, predicate) -> "SearchState":
        bitset = sum(
            1 << deal_id
            for deal_id in self.surviving_deal_ids()
            if predicate(deal_id)
        )
        return replace(self, possible_initial_deals=bitset)

<<<<<<< HEAD
=======
    def normalize_overrides(self) -> "SearchState":
        """Remove overrides already implied by every surviving deal."""
        if not self.possible_initial_deals:
            raise ValueError("cannot normalize an empty information state")

        overrides = list(self.current_owner_override)
        for card in range(TOTAL_CARDS):
            override = overrides[card]
            if override == NO_OVERRIDE:
                continue
            if all(
                INITIAL_DEALS[deal_id].owner_by_card[card] == override
                for deal_id in self.surviving_deal_ids()
            ):
                overrides[card] = NO_OVERRIDE
        return replace(self, current_owner_override=tuple(overrides))

>>>>>>> 4b78765eccd36c34aecb1a0b3ece8cc63c14876e
    def ask(self, asker: int, target: int, card: int | str) -> "SearchState":
        """Apply a question, including the information in asking it.

        ``card`` may be a canonical card index or a label such as ``A1``.
        The question must be compatible with at least one surviving deal.
        """
        card_index = CARD_INDEX[card] if isinstance(card, str) else card
        if asker != self.actor:
            raise ValueError("question asker is not the current actor")
        if asker == target or asker not in range(N_PLAYERS) or target not in range(N_PLAYERS):
            raise ValueError("invalid question players")
<<<<<<< HEAD
=======
        if card_index not in range(TOTAL_CARDS):
            raise ValueError("invalid card")
>>>>>>> 4b78765eccd36c34aecb1a0b3ece8cc63c14876e
        family_start = card_index - (card_index % CARDS_PER_CATEGORY)

        result = self._filter(
            lambda deal_id: (
<<<<<<< HEAD
                # This follows the committed brute-force referee.  The
                # modular referee and architecture.md additionally reject a
                # request for a card the asker already owns; that mismatch is
                # intentionally left visible during this migration.
                any(self.current_owner(deal_id, c) == asker
                    for c in range(family_start, family_start + CARDS_PER_CATEGORY))
=======
                any(self.current_owner(deal_id, c) == asker
                    for c in range(family_start, family_start + CARDS_PER_CATEGORY))
                and self.current_owner(deal_id, card_index) != asker
>>>>>>> 4b78765eccd36c34aecb1a0b3ece8cc63c14876e
            )
        )
        if not result.possible_initial_deals:
            raise ValueError("question is incompatible with every deal")
        return result

    def answer(self, asker: int, target: int, card: int | str, yes: bool) -> "SearchState":
        """Apply an answer and the public YES transfer, if any."""
        card_index = CARD_INDEX[card] if isinstance(card, str) else card
        result = self._filter(
            lambda deal_id: (self.current_owner(deal_id, card_index) == target) == yes
        )
        if not result.possible_initial_deals:
            raise ValueError("answer is incompatible with every deal")
        if yes:
            overrides = list(result.current_owner_override)
            overrides[card_index] = asker
<<<<<<< HEAD
            return replace(result, current_owner_override=tuple(overrides), actor=asker)
=======
            return replace(
                result,
                current_owner_override=tuple(overrides),
                actor=asker,
            ).normalize_overrides()
>>>>>>> 4b78765eccd36c34aecb1a0b3ece8cc63c14876e
        return replace(result, actor=target)

    def replay(self, events: Iterable[object]) -> "SearchState":
        """Replay reference-referee ``Question``/``Answer`` events.

        This is intentionally a small adapter: reference events use zero-based
        players and card labels, exactly as this state does.
        """
        from .referee import Answer, Question

        state = self
        pending = None
        for event in events:
            if isinstance(event, Question):
                if pending is not None:
                    raise ValueError("question before previous answer")
                state = state.ask(event.asker, event.target, event.card)
                pending = event
            elif isinstance(event, Answer):
                if pending is None:
                    raise ValueError("answer without question")
                state = state.answer(
                    pending.asker, pending.target, pending.card, event.value
                )
                pending = None
            else:
                raise TypeError(f"unknown event type: {type(event)!r}")
        return state

    @classmethod
    def from_game_state(cls, state, *, actor: int | None = None) -> "SearchState":
        """Adapt the existing factorized referee state when it is representable.

        The adapter derives ``D`` from the old category worlds and derives a
        single public override per card.  It does not alter the old referee.
        """
        overrides = [NO_OVERRIDE] * TOTAL_CARDS
        allowed = []
        for deal in INITIAL_DEALS:
            ok = True
            for category_index, category in enumerate(state.categories):
                start = category_index * CARDS_PER_CATEGORY
                matching = [world for world in category.worlds
                            if tuple(owner - 1 for owner in world.initial)
                            == deal.owner_by_card[start:start + CARDS_PER_CATEGORY]]
                if not matching:
                    ok = False
                    break
                currents = {tuple(owner - 1 for owner in world.current)
                            for world in matching}
                if len(currents) != 1:
                    raise ValueError("old state does not have a public T")
                current = next(iter(currents))
                for offset, owner in enumerate(current):
                    initial = deal.owner_by_card[start + offset]
                    if owner != initial:
                        if overrides[start + offset] not in (NO_OVERRIDE, owner):
                            raise ValueError("inconsistent public transfer")
                        overrides[start + offset] = owner
            if ok:
                allowed.append(deal.deal_id)
        bitset = sum(1 << deal_id for deal_id in allowed)
<<<<<<< HEAD
        return cls(bitset, tuple(overrides),
                   state.turn - 1 if actor is None else actor)
=======
        return cls(
            bitset,
            tuple(overrides),
            state.turn - 1 if actor is None else actor,
        ).normalize_overrides()
>>>>>>> 4b78765eccd36c34aecb1a0b3ece8cc63c14876e


__all__ = ["NO_OVERRIDE", "SearchState"]

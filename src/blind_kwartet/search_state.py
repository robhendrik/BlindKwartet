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
    INITIAL_OWNER_MASKS,
    N_CATEGORIES,
    N_PLAYERS,
    TOTAL_CARDS,
    deal_ids,
)
from .exceptions import SearchInvariantError
from .moves import AnswerMove, Move, NO, QuestionMove, QuartetMove, YES

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
        if card_index not in range(TOTAL_CARDS):
            raise ValueError("invalid card")
        if deal_id not in range(len(INITIAL_DEALS)):
            raise ValueError("invalid deal id")
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

    def _category_cards(self, category: int) -> range:
        if category not in range(N_CATEGORIES):
            raise ValueError("invalid category")
        start = category * CARDS_PER_CATEGORY
        return range(start, start + CARDS_PER_CATEGORY)

    def _has_quartet(self, deal_id: int, category: int, player: int) -> bool:
        return all(
            self.current_owner(deal_id, card) == player
            for card in self._category_cards(category)
        )

    def _owner_mask(self, player: int, card: int) -> int:
        override = self.current_owner_override[card]
        if override != NO_OVERRIDE:
            return self.D if override == player else 0
        return INITIAL_OWNER_MASKS[player][card] & self.D

    def _quartet_mask(self, category: int, player: int) -> int:
        mask = self.D
        for card in self._category_cards(category):
            mask &= self._owner_mask(player, card)
        return mask

    def _forced_holder(self, category: int) -> int | None:
        for player in range(N_PLAYERS):
            if self._quartet_mask(category, player) == self.D:
                return player
        return None

    @property
    def resolved_categories(self) -> frozenset[int]:
        return frozenset(
            category for category in range(N_CATEGORIES)
            if self._forced_holder(category) is not None
        )

    def forced_quartets(self) -> tuple[QuartetMove, ...]:
        return tuple(
            QuartetMove(category)
            for category in range(N_CATEGORIES)
            if self._forced_holder(category) is not None
        )

    def quartet_holders(self) -> tuple[int | None, ...]:
        return tuple(
            self._forced_holder(category)
            for category in range(N_CATEGORIES)
        )

    @property
    def quartet_scores(self) -> tuple[int, ...]:
        scores = [0] * N_PLAYERS
        for holder in self.quartet_holders():
            if holder is not None:
                scores[holder] += 1
        return tuple(scores)

    @property
    def scores(self) -> tuple[int, ...]:
        return self.quartet_scores

    @property
    def is_terminal(self) -> bool:
        return len(self.resolved_categories) == N_CATEGORIES

    @property
    def terminal(self) -> bool:
        return self.is_terminal

    def _mask(self, predicate) -> int:
        return sum(
            1 << deal_id
            for deal_id in self.surviving_deal_ids()
            if predicate(deal_id)
        )

    def _silence_mask(self, actor: int) -> int:
        resolved = self.resolved_categories
        quartet_worlds = 0
        for category in range(N_CATEGORIES):
            if category not in resolved:
                quartet_worlds |= self._quartet_mask(category, actor)
        return self.D & ~quartet_worlds

    def _validate_move(self, move: QuestionMove) -> None:
        if not isinstance(move, QuestionMove):
            raise TypeError("expected QuestionMove")
        if move.target not in range(N_PLAYERS) or move.target == self.actor:
            raise ValueError("invalid question target")
        if move.category not in range(N_CATEGORIES):
            raise ValueError("invalid question category")
        if move.card not in self._category_cards(move.category):
            raise ValueError("card is not in question category")

    def _question_context(self, move: QuestionMove) -> "QuestionContext":
        self._validate_move(move)
        if move.category in self.resolved_categories:
            raise ValueError("category is already resolved")
        silenced = replace(
            self,
            possible_initial_deals=self._silence_mask(self.actor),
        )
        family_mask = 0
        for card in silenced._category_cards(move.category):
            family_mask |= silenced._owner_mask(self.actor, card)
        question_mask = silenced.D & family_mask & ~silenced._owner_mask(
            self.actor, move.card
        )
        if not question_mask:
            raise ValueError("question is incompatible with every deal")
        questioned = replace(silenced, possible_initial_deals=question_mask)
        yes_mask = questioned._owner_mask(move.target, move.card)
        no_mask = questioned.D & ~yes_mask
        return QuestionContext(questioned, move, yes_mask, no_mask)

    def legal_questions(self) -> tuple[QuestionMove, ...]:
        if self.is_terminal:
            return ()
        moves = []
        for category in range(N_CATEGORIES):
            if category in self.resolved_categories:
                continue
            for target in range(N_PLAYERS):
                if target == self.actor:
                    continue
                for card in self._category_cards(category):
                    try:
                        self._question_context(QuestionMove(target, category, card))
                    except ValueError:
                        continue
                    moves.append(QuestionMove(target, category, card))
        return tuple(moves)

    def _legal_questions_for(self, actor: int) -> tuple[QuestionMove, ...]:
        return replace(self, actor=actor).legal_questions()

    def legal_quartets(self) -> tuple[QuartetMove, ...]:
        if self.is_terminal:
            return ()
        moves = []
        for category in range(N_CATEGORIES):
            if category in self.resolved_categories:
                continue
            if self._quartet_mask(category, self.actor):
                moves.append(QuartetMove(category))
        return tuple(moves)

    def _legal_actions_for(self, actor: int) -> tuple[Move, ...]:
        state = replace(self, actor=actor)
        return state.legal_questions() + state.legal_quartets()

    def legal_moves(self) -> tuple[Move, ...]:
        return self._legal_actions_for(self.actor)

    def stabilize(self, nominal_actor: int | None = None) -> "SearchState":
        """Resolve derived forced quartets and skip actors with no action."""
        actor = self.actor if nominal_actor is None else nominal_actor
        if self.is_terminal:
            return replace(self, actor=actor)
        for offset in range(N_PLAYERS):
            candidate = (actor + offset) % N_PLAYERS
            if self._legal_actions_for(candidate):
                return replace(self, actor=candidate)
        raise SearchInvariantError(
            "unresolved categories have no legal action for any player"
        )

    def resolve_forced_quartets(self) -> "SearchState":
        return self.stabilize(self.actor)

    def apply_question(self, move: QuestionMove) -> "QuestionContext":
        return self._question_context(move)

    def apply_quartet(self, move: QuartetMove) -> "SearchState":
        if not isinstance(move, QuartetMove):
            raise TypeError("expected QuartetMove")
        if move.category not in range(N_CATEGORIES):
            raise ValueError("invalid quartet category")
        if move.category in self.resolved_categories:
            raise ValueError("category is already resolved")
        mask = self._mask(
            lambda deal_id: self._has_quartet(deal_id, move.category, self.actor)
        )
        if not mask:
            raise ValueError("quartet declaration is incompatible with every deal")
        return replace(self, possible_initial_deals=mask).normalize_overrides().stabilize(
            self.actor
        )
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
        if card_index not in range(TOTAL_CARDS):
            raise ValueError("invalid card")
        return self.apply_question(
            QuestionMove(target, card_index // CARDS_PER_CATEGORY, card_index)
        ).state

    def answer(self, asker: int, target: int, card: int | str, yes: bool) -> "SearchState":
        """Apply an answer and the public YES transfer, if any."""
        card_index = CARD_INDEX[card] if isinstance(card, str) else card
        result = self._mask(
            lambda deal_id: (self.current_owner(deal_id, card_index) == target) == yes
        )
        if not result:
            raise ValueError("answer is incompatible with every deal")
        if yes:
            overrides = list(self.current_owner_override)
            overrides[card_index] = asker
            return replace(
                self,
                possible_initial_deals=result,
                current_owner_override=tuple(overrides),
                actor=asker,
            ).normalize_overrides().stabilize(asker)
        return replace(self, possible_initial_deals=result, actor=target).stabilize(target)

    def replay(self, events: Iterable[object]) -> "SearchState":
        """Replay reference-referee ``Question``/``Answer`` events.

        This is intentionally a small adapter: reference events use zero-based
        players and card labels, exactly as this state does.
        """
        from .referee import Answer, Question

        state = self
        pending: QuestionContext | None = None
        for event in events:
            if isinstance(event, Question):
                if pending is not None:
                    raise ValueError("question before previous answer")
                card = CARD_INDEX[event.card]
                pending = state.apply_question(
                    QuestionMove(
                        event.target,
                        card // CARDS_PER_CATEGORY,
                        card,
                    )
                )
            elif isinstance(event, Answer):
                if pending is None:
                    raise ValueError("answer without question")
                state = pending.apply_answer(AnswerMove(event.value))
                pending = None
            else:
                raise TypeError(f"unknown event type: {type(event)!r}")
        return pending.state if pending is not None else state

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
        return cls(
            bitset,
            tuple(overrides),
            state.turn - 1 if actor is None else actor,
        ).normalize_overrides()


@dataclass(frozen=True)
class QuestionContext:
    """Transient answer node; it is not part of the strategic state."""

    state: SearchState
    question: QuestionMove
    yes_mask: int
    no_mask: int

    @property
    def D_yes(self) -> int:
        return self.yes_mask

    @property
    def D_no(self) -> int:
        return self.no_mask

    def legal_answers(self) -> tuple[AnswerMove, ...]:
        answers = []
        if self.yes_mask:
            answers.append(YES)
        if self.no_mask:
            answers.append(NO)
        return tuple(answers)

    def legal_answer_moves(self) -> tuple[AnswerMove, ...]:
        return self.legal_answers()

    def apply_answer(self, answer: AnswerMove) -> SearchState:
        if not isinstance(answer, AnswerMove):
            raise TypeError("expected AnswerMove")
        if answer.yes and not self.yes_mask:
            raise ValueError("YES is incompatible with every deal")
        if not answer.yes and not self.no_mask:
            raise ValueError("NO is incompatible with every deal")
        if answer.yes:
            overrides = list(self.state.T)
            overrides[self.question.card] = self.state.actor
            return replace(
                self.state,
                possible_initial_deals=self.yes_mask,
                current_owner_override=tuple(overrides),
                actor=self.state.actor,
            ).normalize_overrides().stabilize(self.state.actor)
        return replace(
            self.state,
            possible_initial_deals=self.no_mask,
            actor=self.question.target,
        ).stabilize(self.question.target)

    def answer(self, answer: AnswerMove) -> SearchState:
        return self.apply_answer(answer)


__all__ = [
    "AnswerMove",
    "NO",
    "NO_OVERRIDE",
    "QuestionContext",
    "QuestionMove",
    "QuartetMove",
    "SearchInvariantError",
    "SearchState",
    "YES",
]

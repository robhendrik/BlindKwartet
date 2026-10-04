"""Minimal playable Game orchestration over the pure SearchState layer."""

from __future__ import annotations

from collections.abc import Iterable

from .deals import N_PLAYERS
from .exceptions import IllegalMove
from .history import AnswerEvent, GameEvent, QuartetEvent, QuestionEvent
from .moves import AnswerMove, QuestionMove, QuartetMove
from .players import Player, PlayerView
from .result import GameResult
from .search_state import QuestionContext, SearchState


class Game:
    """Run one public game without embedding strategy or rule logic."""

    def __init__(
        self,
        players: Iterable[Player],
        *,
        first_player: int = 0,
        seed: int | None = None,
        max_events: int | None = 10_000,
    ) -> None:
        self.players = tuple(players)
        if len(self.players) != N_PLAYERS:
            raise ValueError(f"expected {N_PLAYERS} players")
        if first_player not in range(N_PLAYERS):
            raise ValueError("invalid first player")
        if max_events is not None and max_events < 0:
            raise ValueError("max_events must be non-negative or None")
        if any(not callable(getattr(player, "play", None)) for player in self.players):
            raise TypeError("each player must provide play(view)")
        self.seed = seed
        self.max_events = max_events
        self.state = SearchState.initial(first_player).resolve_forced_quartets()
        self._history: list[GameEvent] = []
        self._result: GameResult | None = None

    @property
    def history(self) -> tuple[GameEvent, ...]:
        return tuple(self._history)

    def _result_for(self, reason: str) -> GameResult:
        state = self.state.resolve_forced_quartets()
        self.state = state
        scores = state.quartet_scores
        winners = (
            tuple(index for index, score in enumerate(scores)
                  if score == max(scores))
            if reason == "terminal" else ()
        )
        return GameResult(
            final_state=state,
            seat_scores=scores,
            winner_seats=winners,
            n_events=len(self._history),
            end_reason=reason,
            seed=self.seed,
            history=tuple(self._history),
        )

    def _event_limit_reached(self, additional_events: int = 1) -> bool:
        return (
            self.max_events is not None
            and len(self._history) + additional_events > self.max_events
        )

    def _choose(self, player_id: int, state: SearchState, actions: tuple) -> object:
        view = PlayerView(
            player_id=player_id,
            state=state,
            legal_actions=tuple(actions),
            history=tuple(self._history),
        )
        return self.players[player_id].play(view)

    @staticmethod
    def _require_choice(choice: object, actions: tuple, phase: str) -> None:
        if choice not in actions:
            raise IllegalMove(f"player chose an illegal {phase}: {choice!r}")

    def run(self) -> GameResult:
        """Run until terminal or the defensive event limit is reached."""
        if self._result is not None:
            return self._result

        while True:
            self.state = self.state.resolve_forced_quartets()
            if self.state.is_terminal:
                self._result = self._result_for("terminal")
                return self._result
            if self._event_limit_reached():
                self._result = self._result_for("event_limit")
                return self._result

            actions = self.state.legal_moves()
            if not actions:
                # SearchState owns the invariant failure; this is not a normal
                # incomplete-game result.
                self.state = self.state.resolve_forced_quartets()
                actions = self.state.legal_moves()
                if not actions:
                    raise AssertionError("stable unresolved state has no action")

            actor = self.state.actor
            choice = self._choose(actor, self.state, actions)
            self._require_choice(choice, actions, "action")

            if isinstance(choice, QuestionMove):
                if self._event_limit_reached(2):
                    self._result = self._result_for("event_limit")
                    return self._result
                context = self.state.apply_question(choice)
                self._history.append(
                    QuestionEvent(actor, choice.target, choice.category, choice.card)
                )
                answer_actions = context.legal_answers()
                if len(answer_actions) == 1:
                    answer = answer_actions[0]
                else:
                    answer = self._choose(choice.target, context.state, answer_actions)
                    self._require_choice(answer, answer_actions, "answer")
                self._history.append(
                    AnswerEvent(
                        actor,
                        choice.target,
                        choice.category,
                        choice.card,
                        answer.yes,
                    )
                )
                self.state = context.apply_answer(answer)
            elif isinstance(choice, QuartetMove):
                if self._event_limit_reached():
                    self._result = self._result_for("event_limit")
                    return self._result
                self._history.append(QuartetEvent(actor, choice.category))
                self.state = self.state.apply_quartet(choice)
            else:
                raise IllegalMove(f"unsupported stable action: {choice!r}")

    play = run

    @classmethod
    def replay(
        cls,
        history: Iterable[GameEvent],
        *,
        first_player: int = 0,
    ) -> SearchState:
        """Replay structured public events using the same pure rule layer."""
        state = SearchState.initial(first_player).resolve_forced_quartets()
        pending: QuestionContext | None = None
        for event in history:
            if isinstance(event, QuestionEvent):
                if pending is not None:
                    raise ValueError("question before previous answer")
                if event.asker != state.actor:
                    raise ValueError("question event has the wrong actor")
                pending = state.apply_question(
                    QuestionMove(event.target, event.category, event.card)
                )
            elif isinstance(event, AnswerEvent):
                if pending is None:
                    raise ValueError("answer without question")
                if (
                    event.asker != pending.state.actor
                    or event.target != pending.question.target
                    or event.category != pending.question.category
                    or event.card != pending.question.card
                ):
                    raise ValueError("answer event does not match pending question")
                state = pending.apply_answer(AnswerMove(event.yes))
                pending = None
            elif isinstance(event, QuartetEvent):
                if pending is not None:
                    raise ValueError("quartet before previous answer")
                if event.player != state.actor:
                    raise ValueError("quartet event has the wrong actor")
                state = state.apply_quartet(QuartetMove(event.category))
            else:
                raise TypeError(f"unknown game event: {event!r}")
        if pending is not None:
            raise ValueError("history ends with an unanswered question")
        return state.resolve_forced_quartets()


__all__ = ["Game"]

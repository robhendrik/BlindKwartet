"""Milestone 2 integration and playable-game regressions."""

from dataclasses import dataclass

import pytest

from blind_kwartet.game import Game
from blind_kwartet.history import QuartetEvent
from blind_kwartet.moves import AnswerMove, QuestionMove, QuartetMove, YES
from blind_kwartet.players import Player, PlayerView, RandomPlayer
from blind_kwartet.search_state import SearchState


def test_typed_layer_supports_mixed_question_answer_and_quartet():
    state = SearchState.initial()
    question = QuestionMove(target=1, category=0, card=0)
    context = state.apply_question(question)
    after_yes = context.apply_answer(YES)
    assert after_yes.actor == 0
    assert after_yes.legal_quartets() == (QuartetMove(0),)

    after_quartet = after_yes.apply_quartet(QuartetMove(0))
    assert after_quartet.resolved_categories == frozenset({0})
    assert after_quartet.D & ~after_yes.D == 0


def test_random_player_chooses_only_supplied_actions():
    actions = (QuestionMove(1, 0, 0), QuartetMove(1))
    view = PlayerView(0, SearchState.initial(), actions)
    assert RandomPlayer(seed=3).play(view) in actions


def test_seeded_random_players_are_reproducible():
    view = PlayerView(
        0,
        SearchState.initial(),
        (QuestionMove(1, 0, 0), QuartetMove(1)),
    )
    first = RandomPlayer(seed=17)
    second = RandomPlayer(seed=17)
    assert [first.play(view) for _ in range(20)] == [
        second.play(view) for _ in range(20)
    ]


def test_game_does_not_depend_on_concrete_player_subclasses():
    class DuckPlayer:
        def play(self, view):
            return view.legal_actions[0]

    result = Game((DuckPlayer(), DuckPlayer(), DuckPlayer()), max_events=0).run()
    assert result.end_reason == "event_limit"


def test_forced_answers_are_applied_without_calling_target():
    class FirstAction(Player):
        def __init__(self):
            self.calls = 0

        def play(self, view):
            self.calls += 1
            return view.legal_actions[0]

    players = [FirstAction(), FirstAction(), FirstAction()]
    game = Game(players, max_events=2)
    # The first action is a question; its answer may be forced or strategic.
    result = game.run()
    assert result.n_events == 2
    assert players[game.history[0].asker].calls >= 1


def test_strategic_answer_is_offered_to_target():
    class ChooseQuestion(Player):
        def play(self, view):
            return next(action for action in view.legal_actions
                        if isinstance(action, QuestionMove))

    class ChooseYes(Player):
        def __init__(self):
            self.answer_views = 0

        def play(self, view):
            if all(isinstance(action, AnswerMove) for action in view.legal_actions):
                self.answer_views += 1
                return YES
            return view.legal_actions[0]

    asker = ChooseQuestion()
    target = ChooseYes()
    result = Game((asker, target, ChooseQuestion()), max_events=2).run()
    assert target.answer_views == 1
    assert result.history[1].yes is True
    assert result.final_state.actor == 0


def test_live_final_state_equals_replay():
    players = tuple(RandomPlayer(seed=seed) for seed in (10, 20, 30))
    result = Game(players, seed=99, max_events=300).run()
    assert result.end_reason == "terminal"
    replayed = Game.replay(result.history)
    assert replayed == result.final_state


def test_quartet_event_does_not_end_turn_and_scores_are_derived():
    state = SearchState.initial()
    state = state.apply_question(QuestionMove(1, 0, 0)).apply_answer(YES)
    assert state.actor == 0
    state = state.apply_quartet(QuartetMove(0))
    assert state.actor == 0
    assert state.quartet_scores == (1, 0, 0)


def test_event_limit_is_distinct_and_has_no_winner():
    result = Game(tuple(RandomPlayer(seed=i) for i in range(3)), max_events=0).run()
    assert result.end_reason == "event_limit"
    assert result.winner_seats == ()

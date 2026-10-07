from blind_kwartet.game import Game
from blind_kwartet.history import QuestionEvent
from blind_kwartet.moves import AnswerMove, QuestionMove, QuartetMove, YES
from blind_kwartet.players import (
    Player,
    PlayerView,
    RandomPlayer,
    SingleCategoryTreePlayer,
)
from blind_kwartet.search_state import SearchState
from blind_kwartet.single_category_solver import CategoryOutcome, CategoryResult, decode_world


def _known_category_state(owners, category=0):
    state = SearchState.initial()
    start = category * 4
    return state._filter(
        lambda deal_id: tuple(
            state.current_owner(deal_id, start + card) for card in range(4)
        ) == owners
    )


def _question(category, target, card):
    return QuestionMove(target=target, category=category, card=category * 4 + card)


def test_tree_player_is_player_and_returns_supplied_action():
    player = SingleCategoryTreePlayer()
    assert isinstance(player, Player)
    state = _known_category_state((0, 1, 2, 2))
    moves = (_question(0, 1, 1), _question(0, 2, 2))

    chosen = player.play(PlayerView(0, state, moves))

    assert chosen in moves


def test_legal_quartet_is_chosen_before_tree_search():
    state = SearchState.initial().apply_question(
        QuestionMove(target=1, category=0, card=0)
    ).apply_answer(YES)
    player = SingleCategoryTreePlayer()
    quartet = QuartetMove(0)
    moves = (_question(0, 1, 1), quartet)

    assert player.play(PlayerView(0, state, moves)) == quartet
    assert player.moves_evaluated == 0


def test_win_beats_open_and_loss_with_canonical_tie_break(monkeypatch):
    player = SingleCategoryTreePlayer()
    state = SearchState.initial()
    moves = (_question(1, 2, 0), _question(0, 2, 0), _question(2, 1, 0))
    outcomes = {
        moves[0]: CategoryOutcome.OPEN,
        moves[1]: CategoryOutcome.WIN,
        moves[2]: CategoryOutcome.LOSS,
    }
    monkeypatch.setattr(
        player,
        "_evaluate_question",
        lambda _view, move: CategoryResult(outcomes[move]),
    )

    assert player.play(PlayerView(0, state, moves)) == moves[1]
    assert [move for move, _ in player.last_evaluations] == [moves[1], moves[0], moves[2]]


def test_open_beats_loss_and_all_loss_uses_deterministic_order(monkeypatch):
    player = SingleCategoryTreePlayer()
    state = SearchState.initial()
    moves = (_question(1, 2, 0), _question(0, 2, 0), _question(2, 1, 0))
    outcomes = {move: CategoryOutcome.LOSS for move in moves}
    monkeypatch.setattr(
        player,
        "_evaluate_question",
        lambda _view, move: CategoryResult(outcomes[move]),
    )
    assert player.play(PlayerView(0, state, moves)) == moves[1]

    outcomes[moves[0]] = CategoryOutcome.OPEN
    assert player.play(PlayerView(0, state, moves)) == moves[0]


def test_physical_targets_map_to_next_and_third_relative_players(monkeypatch):
    player = SingleCategoryTreePlayer()
    state = _known_category_state((0, 1, 2, 2))
    moves = (_question(0, 0, 1), _question(0, 1, 1))
    captured = []

    def capture(_bitmap, actor, move):
        captured.append((actor, move))
        return CategoryResult(CategoryOutcome.OPEN)

    monkeypatch.setattr(player.solver, "evaluate_move", capture)
    player.play(PlayerView(2, state, moves))

    assert captured == [
        (0, type(captured[0][1])(1, 1)),
        (0, type(captured[1][1])(2, 1)),
    ]


def test_non_first_category_uses_local_card_numbers(monkeypatch):
    player = SingleCategoryTreePlayer()
    state = _known_category_state((2, 0, 1, 2), category=2)
    move = _question(2, 0, 3)
    captured = []

    def capture(bitmap, actor, local_move):
        captured.append((bitmap, actor, local_move))
        return CategoryResult(CategoryOutcome.WIN)

    monkeypatch.setattr(player.solver, "evaluate_move", capture)
    assert player.play(PlayerView(2, state, (move,))) == move
    assert captured[0][1] == 0
    assert captured[0][2].respondent == 1
    assert captured[0][2].card == 3
    assert decode_world(next(index for index in range(81) if captured[0][0] & (1 << index))) == (
        0, 1, 2, 0
    )


def test_answer_views_remain_total_and_choose_no_first():
    player = SingleCategoryTreePlayer()
    state = SearchState.initial().apply_question(
        QuestionMove(target=1, category=0, card=0)
    ).state
    answers = (AnswerMove(False), AnswerMove(True))
    view = PlayerView(
        1,
        state,
        answers,
        history=(QuestionEvent(0, 1, 0, 0),),
    )
    player._evaluate_answer_branch = lambda *_args: CategoryOutcome.OPEN
    assert player.play(view) == AnswerMove(False)


def test_forced_yes_answer_is_returned_without_branch_comparison():
    player = SingleCategoryTreePlayer()
    state = SearchState.initial().apply_question(
        QuestionMove(target=1, category=0, card=0)
    ).state
    view = PlayerView(
        1,
        state,
        (AnswerMove(True),),
        history=(QuestionEvent(0, 1, 0, 0),),
    )

    assert player.play(view) == AnswerMove(True)
    diagnostic = player.decision_diagnostics[-1]
    assert diagnostic.selected_answer is True
    assert diagnostic.yes_outcome is None
    assert diagnostic.no_outcome is None


def test_strategic_answer_strictly_prefers_yes(monkeypatch):
    player = SingleCategoryTreePlayer()
    state = SearchState.initial().apply_question(
        QuestionMove(target=1, category=0, card=0)
    ).state
    view = PlayerView(1, state, (AnswerMove(False), AnswerMove(True)), history=(QuestionEvent(0, 1, 0, 0),))
    outcomes = iter((CategoryOutcome.WIN, CategoryOutcome.LOSS))
    monkeypatch.setattr(player, "_evaluate_answer_branch", lambda *_args: next(outcomes))

    assert player.play(view) == AnswerMove(True)
    diagnostic = player.decision_diagnostics[-1]
    assert diagnostic.yes_outcome is CategoryOutcome.WIN
    assert diagnostic.no_outcome is CategoryOutcome.LOSS
    assert diagnostic.answer_selection_reason == "strict"


def test_strategic_answer_strictly_prefers_no(monkeypatch):
    player = SingleCategoryTreePlayer()
    state = SearchState.initial().apply_question(
        QuestionMove(target=1, category=0, card=0)
    ).state
    view = PlayerView(1, state, (AnswerMove(False), AnswerMove(True)), history=(QuestionEvent(0, 1, 0, 0),))
    outcomes = iter((CategoryOutcome.LOSS, CategoryOutcome.WIN))
    monkeypatch.setattr(player, "_evaluate_answer_branch", lambda *_args: next(outcomes))

    assert player.play(view) == AnswerMove(False)
    assert player.decision_diagnostics[-1].answer_selection_reason == "strict"


def test_strategic_answer_tie_preserves_no(monkeypatch):
    for outcome in CategoryOutcome:
        player = SingleCategoryTreePlayer()
        state = SearchState.initial().apply_question(
            QuestionMove(target=1, category=0, card=0)
        ).state
        view = PlayerView(1, state, (AnswerMove(False), AnswerMove(True)), history=(QuestionEvent(0, 1, 0, 0),))
        monkeypatch.setattr(player, "_evaluate_answer_branch", lambda *_args, outcome=outcome: outcome)

        assert player.play(view) == AnswerMove(False)
        diagnostic = player.decision_diagnostics[-1]
        assert diagnostic.yes_outcome is outcome
        assert diagnostic.no_outcome is outcome
        assert diagnostic.selected_answer is False
        assert diagnostic.answer_selection_reason == "tie"


def test_answer_evaluation_uses_answerer_perspective_and_post_answer_state(monkeypatch):
    player = SingleCategoryTreePlayer()
    state = SearchState.initial().apply_question(
        QuestionMove(target=1, category=0, card=0)
    ).state
    view = PlayerView(1, state, (AnswerMove(False), AnswerMove(True)), history=(QuestionEvent(0, 1, 0, 0),))
    projections = []
    actors = []

    def capture_projection(resulting_state, category, active_player):
        projections.append((resulting_state, category, active_player))
        return 0

    monkeypatch.setattr("blind_kwartet.players.project_category_bitmap", capture_projection)
    monkeypatch.setattr(
        player.solver,
        "solve",
        lambda bitmap, actor: actors.append((bitmap, actor)) or CategoryResult(CategoryOutcome.OPEN),
    )

    player.play(view)

    assert [active_player for _, _, active_player in projections] == [1, 1]
    assert [actor for _, actor in actors] == [2, 0]
    assert projections[0][0].T[0] == 0
    assert projections[1][0].T[0] == -1


def test_broad_entry_state_selects_deterministic_legal_loss():
    state = SearchState.initial()
    state = state._filter(
        lambda deal_id: (
            state.current_owner(deal_id, "A1") != 0
            and 1 <= sum(state.current_owner(deal_id, card) == 0 for card in range(4)) < 4
        )
    )
    legal = tuple(move for move in state.legal_questions() if move.category == 0)
    player = SingleCategoryTreePlayer()

    chosen = player.play(PlayerView(0, state, legal))

    assert chosen == legal[0]
    assert all(result.outcome is CategoryOutcome.LOSS for _, result in player.last_evaluations)
    assert player.solver_nodes > 0
    assert player.solver_memo_hits >= 0
    assert player.solver_cycle_hits >= 0


def test_random_player_and_short_game_remain_compatible():
    players = (
        SingleCategoryTreePlayer(),
        RandomPlayer(seed=11),
        RandomPlayer(seed=22),
    )
    result = Game(players, max_events=6).run()

    assert result.end_reason in {"event_limit", "terminal"}
    assert result.n_events <= 6

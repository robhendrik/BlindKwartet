import pytest

from blind_kwartet.single_category_solver import (
    CategoryOutcome,
    CategoryResult,
    LocalCategoryMove,
    SingleCategorySolver,
    decode_world,
    encode_world,
    world_bit,
)


def broad_entry_bitmap():
    """All fresh-category worlds where P1 can legally ask for A1."""
    return sum(
        world_bit(owners)
        for owners in (decode_world(index) for index in range(81))
        if owners[0] != 0 and 1 <= owners.count(0) < 4
    )


def test_broad_canonical_entry_bitmap_has_exact_count_triples():
    bitmap = broad_entry_bitmap()
    worlds = [decode_world(index) for index in range(81) if bitmap & (1 << index)]
    triples = {tuple(owners.count(owner) for owner in range(3)) for owners in worlds}
    expected = {
        (1, 3, 0), (1, 0, 3), (1, 2, 1), (1, 1, 2),
        (2, 2, 0), (2, 0, 2), (2, 1, 1), (3, 1, 0), (3, 0, 1),
    }
    assert triples == expected
    assert all(owners[0] != 0 and 1 <= owners.count(0) < 4 for owners in worlds)


def test_canonical_line_reduces_to_unique_entry_world():
    solver = SingleCategorySolver()
    candidates = [
        (owners, owners)
        for index in solver._set_bits(broad_entry_bitmap())
        for owners in [decode_world(index)]
    ]
    actor = 0
    transcript = (
        (0, 1, 0, False),
        (1, 2, 0, True),
        (1, 2, 1, False),
        (2, 0, 1, True),
        (2, 1, 0, True),
        (2, 1, 2, True),
    )

    for asker, respondent, card, yes in transcript:
        assert actor == asker
        move = LocalCategoryMove(respondent, card)
        before_bitmap = sum(world_bit(current) for _, current in candidates)
        assert solver._legal_question_bitmap(before_bitmap, asker, move)
        next_candidates = []
        for initial, current in candidates:
            legal = actor in current and current[card] != actor
            if not legal:
                continue
            if yes != (current[card] == respondent):
                continue
            updated = list(current)
            if yes:
                updated[card] = actor
            next_candidates.append((initial, tuple(updated)))
        assert next_candidates
        candidates = next_candidates
        actor = asker if yes else respondent

    assert {initial for initial, _ in candidates} == {(2, 0, 1, 2)}
    assert {current for _, current in candidates} == {(2, 2, 2, 2)}
    assert actor == 2


def test_broad_entry_diagnostic_reports_root_behavior():
    bitmap = broad_entry_bitmap()
    solver = SingleCategorySolver()
    moves = solver._legal_moves(bitmap, 0)
    assert moves

    print(f"broad entry worlds={bitmap.bit_count()} legal_first_asks={len(moves)}")
    for move in moves:
        result = solver.evaluate_move(bitmap, 0, move)
        print(
            f"ask P1->P{move.respondent + 1} A{move.card + 1}: "
            f"{result.outcome.value} distance=n/a"
        )
    print(
        f"nodes={solver.nodes} memo_hits={solver.memo_hits} "
        f"cycle_hits={solver.cycle_hits}"
    )


def test_encode_decode_all_worlds():
    for index in range(81):
        owners = decode_world(index)
        assert encode_world(owners) == index


def test_act_of_asking_filters_illegal_worlds():
    solver = SingleCategorySolver()
    bitmap = world_bit((1, 0, 2, 2)) | world_bit((1, 1, 2, 2))
    move = LocalCategoryMove(respondent=1, card=0)

    # The second world is illegal because P1 has no category card.  In the
    # first world P1 has a card and does not own A1, so the ask is legal.
    assert solver._legal_question_bitmap(bitmap, 0, move) == world_bit((1, 0, 2, 2))


def test_yes_filters_and_transfers_and_no_changes_actor():
    solver = SingleCategorySolver()
    bitmap = world_bit((1, 0, 2, 2)) | world_bit((2, 0, 2, 2))
    move = LocalCategoryMove(respondent=1, card=0)
    seen = []

    def capture(next_bitmap, next_actor):
        seen.append((next_bitmap, next_actor))
        return CategoryResult(CategoryOutcome.OPEN)

    solver._solve = capture  # type: ignore[method-assign]
    solver.evaluate_move(bitmap, 0, move)
    assert (world_bit((0, 0, 2, 2)), 0) in seen
    assert (world_bit((2, 0, 2, 2)), 1) in seen


def test_impossible_yes_branch_makes_local_question_illegal():
    solver = SingleCategorySolver()
    bitmap = world_bit((2, 2, 0, 2))
    seen = []
    solver._solve = lambda next_bitmap, next_actor: seen.append(
        (next_bitmap, next_actor)
    ) or CategoryResult(CategoryOutcome.WIN)  # type: ignore[method-assign]

    move = LocalCategoryMove(1, 0)
    assert solver._legal_question_bitmap(bitmap, 0, move) == 0
    with pytest.raises(ValueError):
        solver.evaluate_move(bitmap, 0, move)
    assert seen == []


def test_move_branch_combinations_use_worst_answer(monkeypatch):
    solver = SingleCategorySolver()
    bitmap = world_bit((1, 0, 2, 2)) | world_bit((2, 0, 2, 2))
    move = LocalCategoryMove(1, 0)

    for expected, branches in (
        (CategoryOutcome.WIN, [CategoryOutcome.WIN, CategoryOutcome.WIN]),
        (CategoryOutcome.OPEN, [CategoryOutcome.WIN, CategoryOutcome.OPEN]),
        (CategoryOutcome.LOSS, [CategoryOutcome.WIN, CategoryOutcome.LOSS]),
    ):
        values = iter(branches)
        monkeypatch.setattr(
            solver,
            "_solve",
            lambda _bitmap, _actor: CategoryResult(next(values)),
        )
        assert solver.evaluate_move(bitmap, 0, move).outcome is expected


def test_singleton_quartets_are_terminal():
    solver = SingleCategorySolver()
    assert solver.solve(world_bit((0, 0, 0, 0))).outcome is CategoryOutcome.WIN
    assert solver.solve(world_bit((1, 1, 1, 1))).outcome is CategoryOutcome.LOSS
    assert solver.solve(world_bit((2, 2, 2, 2))).outcome is CategoryOutcome.LOSS


def test_repeated_state_on_recursion_stack_is_open():
    solver = SingleCategorySolver()
    move = LocalCategoryMove(1, 0)
    solver._legal_moves = lambda _bitmap, _actor: (move,)  # type: ignore[method-assign]
    solver._evaluate_move = lambda bitmap, actor, _move: solver._solve(  # type: ignore[method-assign]
        bitmap, actor
    )
    assert solver.solve(world_bit((0, 1, 2, 2))).outcome is CategoryOutcome.OPEN
    assert solver.cycle_hits == 1


def test_recursion_cycle_is_not_memoized_until_evaluation_completes():
    solver = SingleCategorySolver()
    state = (world_bit((0, 1, 2, 2)), 0)
    move = LocalCategoryMove(1, 0)
    solver._legal_moves = lambda _bitmap, _actor: (move,)  # type: ignore[method-assign]
    observed_memo_membership = []

    def recurse(bitmap, actor, _move):
        observed_memo_membership.append((bitmap, actor) in solver.memo)
        return solver._solve(bitmap, actor)

    solver._evaluate_move = recurse  # type: ignore[method-assign]
    assert solver.solve(*state).outcome is CategoryOutcome.OPEN
    assert observed_memo_membership == [False]
    assert state in solver.memo


def test_no_legal_category_move_is_open():
    # P1 owns no card in this category, so the real game would move on to
    # another category; this local model reports OPEN.
    bitmap = world_bit((1, 1, 2, 2))
    assert SingleCategorySolver().solve(bitmap).outcome is CategoryOutcome.OPEN


def test_memoized_result_agrees_with_fresh_evaluation():
    bitmap = world_bit((1, 0, 2, 2)) | world_bit((2, 0, 2, 2))
    solver = SingleCategorySolver()
    first = solver.solve(bitmap)
    second = solver.solve(bitmap)
    fresh = SingleCategorySolver().solve(bitmap)
    assert first == fresh == second
    assert solver.memo_hits >= 1

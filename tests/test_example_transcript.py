import pytest

from blind_kwartet import Answer, GameEngine, IllegalEvent, RawQuestion


def test_example_transcript_forces_third_answer_yes():
    engine = GameEngine()

    engine.ask(RawQuestion(1, 2, "Bloemen", "Roos"))
    engine.answer(Answer(False))

    engine.ask(RawQuestion(2, 1, "Bloemen", "Tulp"))
    engine.answer(Answer(False))

    assert len(engine.state.categories[0].worlds) == 2
    assert engine.state.categories[0].counts == {(1, 1, 2)}

    engine.ask(RawQuestion(1, 2, "Bloemen", "Lelie"))
    assert len(engine.state.categories[0].worlds) == 1

    world = engine.state.categories[0].worlds[0]
    assert world.initial == (3, 3, 2, 1)
    assert world.current[2] == 2

    engine.answer(Answer(True))

    world = engine.state.categories[0].worlds[0]
    assert world.initial == (3, 3, 2, 1)
    assert world.current == (3, 3, 1, 1)


def test_forced_third_no_is_illegal_and_rolls_back():
    engine = GameEngine()

    engine.ask(RawQuestion(1, 2, "Bloemen", "Roos"))
    engine.answer(Answer(False))
    engine.ask(RawQuestion(2, 1, "Bloemen", "Tulp"))
    engine.answer(Answer(False))
    engine.ask(RawQuestion(1, 2, "Bloemen", "Lelie"))

    before = engine.global_hypothesis_count()

    with pytest.raises(IllegalEvent):
        engine.answer(Answer(False))

    assert engine.global_hypothesis_count() == before
    assert engine.state.pending_question is not None


def test_count_information_propagates_to_other_categories():
    engine = GameEngine()

    engine.ask(RawQuestion(1, 2, "Bloemen", "Roos"))
    engine.answer(Answer(False))
    engine.ask(RawQuestion(2, 1, "Bloemen", "Tulp"))
    engine.answer(Answer(False))

    assert engine.state.categories[0].counts == {(1, 1, 2)}
    assert len(engine.state.categories[1].counts) == 10
    assert len(engine.state.categories[2].counts) == 10
    assert len(engine.state.categories[1].worlds) == 70
    assert len(engine.state.categories[2].worlds) == 70

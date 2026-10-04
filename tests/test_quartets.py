import pytest

from blind_kwartet import (
    Answer,
    GameEngine,
    IllegalEvent,
    QuartetDeclaration,
    RawQuestion,
)


def test_player_can_declare_quartet_when_possible_but_not_forced():
    engine = GameEngine()

    engine.ask(RawQuestion(1, 2, "Bloemen", "Roos"))
    engine.answer(Answer(True))

    assert not engine.state.categories[0].completed

    category = engine.declare_quartet(QuartetDeclaration(1, "Bloemen"))

    assert category == 0
    assert engine.state.categories[0].completed
    assert engine.state.categories[0].scored_by == 1
    assert engine.state.score(1) == 1
    assert all(
        world.current == (1, 1, 1, 1)
        for world in engine.state.categories[0].worlds
    )


def test_silence_before_next_question_removes_unannounced_quartet_worlds():
    engine = GameEngine()

    engine.ask(RawQuestion(1, 2, "Bloemen", "Roos"))
    engine.answer(Answer(True))

    assert any(
        len(set(world.current)) == 1
        for world in engine.state.categories[0].worlds
    )

    engine.ask(RawQuestion(1, 2, "Schepen", "Titanic"))

    assert all(
        len(set(world.current)) != 1
        for world in engine.state.categories[0].worlds
    )


def test_impossible_quartet_declaration_rolls_back():
    engine = GameEngine()
    before = engine.global_hypothesis_count()

    with pytest.raises(IllegalEvent):
        engine.declare_quartet(QuartetDeclaration(1, "Bloemen"))

    assert engine.global_hypothesis_count() == before
    assert engine.state.naming.category_names == {}


def test_completed_category_cannot_be_asked_about():
    engine = GameEngine()

    engine.ask(RawQuestion(1, 2, "Bloemen", "Roos"))
    engine.answer(Answer(True))
    engine.declare_quartet(QuartetDeclaration(1, "Bloemen"))

    with pytest.raises(IllegalEvent):
        engine.ask(RawQuestion(1, 2, "Bloemen", "Tulp"))

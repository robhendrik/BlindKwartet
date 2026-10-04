import pytest

from blind_kwartet import Answer, GameEngine, IllegalEvent, RawQuestion


def test_first_names_become_A1_then_A2_then_B1():
    engine = GameEngine()

    q1 = engine.ask(RawQuestion(1, 2, "Bloemen", "Roos"))
    assert (q1.category, q1.card) == (0, 0)
    engine.answer(Answer(False))

    q2 = engine.ask(RawQuestion(2, 1, "Bloemen", "Tulp"))
    assert (q2.category, q2.card) == (0, 1)
    engine.answer(Answer(False))

    q3 = engine.ask(RawQuestion(1, 2, "Schepen", "Titanic"))
    assert (q3.category, q3.card) == (1, 0)


def test_mapping_is_transactional_when_question_is_illegal():
    engine = GameEngine()

    with pytest.raises(IllegalEvent):
        engine.ask(RawQuestion(2, 1, "Bloemen", "Roos"))

    assert engine.state.naming.category_names == {}
    assert engine.state.naming.card_names == {}

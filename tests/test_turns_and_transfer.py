from blind_kwartet import Answer, GameEngine, RawQuestion


def test_no_passes_turn_to_answerer():
    engine = GameEngine()
    engine.ask(RawQuestion(1, 2, "Bloemen", "Roos"))
    engine.answer(Answer(False))
    assert engine.state.turn == 2


def test_yes_keeps_turn_with_asker_and_transfers_card():
    engine = GameEngine()
    engine.ask(RawQuestion(1, 2, "Bloemen", "Roos"))
    engine.answer(Answer(True))

    assert engine.state.turn == 1
    for world in engine.state.categories[0].worlds:
        assert world.initial[0] == 2
        assert world.current[0] == 1

from blind_kwartet import GameConfig, GameEngine
from blind_kwartet.state import generate_category_worlds, generate_count_patterns


def test_default_category_has_78_worlds_and_12_counts():
    config = GameConfig()
    assert len(generate_category_worlds(config)) == 78
    assert len(generate_count_patterns(config)) == 12


def test_default_factorized_state_represents_34032_global_deals():
    engine = GameEngine()
    assert engine.category_snapshot() == {
        0: (78, 12, False),
        1: (78, 12, False),
        2: (78, 12, False),
    }
    assert engine.global_hypothesis_count() == 34_032


def test_category_generation_generalizes_to_4_players_4_categories():
    config = GameConfig(n_players=4, n_categories=4, cards_per_category=4)
    assert len(generate_category_worlds(config)) == 252
    assert len(generate_count_patterns(config)) == 31

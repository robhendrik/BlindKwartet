from math import log2

from scripts.play_random_game_verbose import entropy_bits, information_gain


def test_verbose_information_helpers_use_exact_world_counts():
    assert entropy_bits(34032) == log2(34032)
    assert information_gain(34032, 17016) == log2(2)
    assert information_gain(10, 10) == 0


def test_verbose_fixed_seed_game_completes_or_hits_event_limit():
    from blind_kwartet.game import Game
    from blind_kwartet.players import RandomPlayer

    result = Game(
        tuple(RandomPlayer(seed=100 + seat) for seat in range(3)),
        seed=123,
        max_events=300,
    ).run()
    assert result.end_reason in {"terminal", "event_limit"}
    assert result.final_state.D.bit_count() > 0

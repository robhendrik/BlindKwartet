"""Run a reproducible compact random Blind Kwartet game."""

from blind_kwartet.game import Game
from blind_kwartet.players import RandomPlayer
from blind_kwartet.history import AnswerEvent, QuartetEvent, QuestionEvent


def main() -> None:
    players = tuple(RandomPlayer(seed=100 + seat) for seat in range(3))
    result = Game(players, seed=123, max_events=300).run()
    for event in result.history:
        if isinstance(event, QuestionEvent):
            print(f"P{event.asker + 1} asks P{event.target + 1} for {event.category}:{event.card}")
        elif isinstance(event, AnswerEvent):
            print(f"P{event.target + 1} answers {'YES' if event.yes else 'NO'}")
        elif isinstance(event, QuartetEvent):
            print(f"P{event.player + 1} declares quartet {event.category}")
    print(f"end={result.end_reason} scores={result.seat_scores} events={result.n_events}")


if __name__ == "__main__":
    main()

"""Demonstration of the modular Blind Kwartet referee."""

from blind_kwartet import Answer, GameEngine, RawQuestion
from blind_kwartet.naming import canonical_card_label


def show(engine: GameEngine, title: str) -> None:
    print(title)
    print(f"  turn: P{engine.state.turn}")
    print(f"  global hypotheses: {engine.global_hypothesis_count():,}")
    for category, (worlds, counts, completed) in engine.category_snapshot().items():
        label = chr(ord("A") + category)
        print(
            f"  {label}: {worlds:2} detailed, "
            f"{counts:2} counts, completed={completed}"
        )
    print()


engine = GameEngine()
show(engine, "Initial state")

q = engine.ask(RawQuestion(1, 2, "Bloemen", "Roos"))
print("Mapped first question to:", canonical_card_label(q.category, q.card))
show(engine, "After Q1")

engine.answer(Answer(False))
show(engine, "After NO")

engine.ask(RawQuestion(2, 1, "Bloemen", "Tulp"))
show(engine, "After Q2")

engine.answer(Answer(False))
show(engine, "After NO")

engine.ask(RawQuestion(1, 2, "Bloemen", "Lelie"))
show(engine, "After Q3")

engine.answer(Answer(True))
show(engine, "After forced YES")

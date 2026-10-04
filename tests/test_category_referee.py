from blind_kwartet.category_referee import (
    Question,
    Answer,
    run_transcript,
)

def test_transcript():
    transcript = [
        Question(asker=1, target=2, card=1),
        Answer(yes=False),

        Question(asker=2, target=1, card=2),
        Answer(yes=False),

        Question(asker=1, target=2, card=3),
        Answer(yes=True),
    ]

    run_transcript(transcript)
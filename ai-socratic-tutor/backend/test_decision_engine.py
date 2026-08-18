from app.services.decision_engine import decide_next_action


tests = [
    {
        "evaluation": "correct",
        "understanding": "intermediate",
        "hint_level": 0,
        "confidence": 0.95,
    },
    {
        "evaluation": "misconception",
        "understanding": "beginner",
        "hint_level": 0,
        "confidence": 0.90,
    },
    {
        "evaluation": "incorrect",
        "understanding": "developing",
        "hint_level": 1,
        "confidence": 0.92,
    },
    {
        "evaluation": "incorrect",
        "understanding": "developing",
        "hint_level": 3,
        "confidence": 0.95,
    },
    {
        "evaluation": "not_attempted",
        "understanding": "beginner",
        "hint_level": 0,
        "confidence": 0.90,
    },
]


for test in tests:

    decision = decide_next_action(**test)

    print("\nInput:")
    print(test)

    print("Decision:")
    print(decision)
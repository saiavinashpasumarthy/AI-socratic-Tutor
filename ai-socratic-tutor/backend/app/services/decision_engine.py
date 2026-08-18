from dataclasses import dataclass


@dataclass
class Decision:
    action: str
    hint_level: int


def decide_next_action(
    evaluation: str,
    understanding: str,
    hint_level: int,
    confidence: float,
) -> Decision:

    evaluation = evaluation.lower()
    understanding = understanding.lower()

    # -----------------------------------------
    # 1. Student is correct
    # -----------------------------------------

    if evaluation == "correct":

        return Decision(
            action="practice",
            hint_level=0,
        )

    # -----------------------------------------
    # 2. Student has a misconception
    # -----------------------------------------

    if evaluation == "misconception":

        return Decision(
            action="clarify",
            hint_level=min(hint_level + 1, 3),
        )

    # -----------------------------------------
    # 3. Student is partially correct
    # -----------------------------------------

    if evaluation == "partially_correct":

        return Decision(
            action="guide",
            hint_level=min(hint_level + 1, 3),
        )

    # -----------------------------------------
    # 4. Student is incorrect
    # -----------------------------------------

    if evaluation == "incorrect":

        return Decision(
            action="hint",
            hint_level=min(hint_level + 1, 3),
        )

    # -----------------------------------------
    # 5. Student hasn't attempted yet
    # -----------------------------------------

    if evaluation == "not_attempted":

        return Decision(
            action="guide",
            hint_level=hint_level,
        )

    # -----------------------------------------
    # 6. Unknown evaluation
    # -----------------------------------------

    if confidence < 0.5:

        return Decision(
            action="clarify",
            hint_level=hint_level,
        )

    # -----------------------------------------
    # 7. Default
    # -----------------------------------------

    return Decision(
        action="guide",
        hint_level=hint_level,
    )
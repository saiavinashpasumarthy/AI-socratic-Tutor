from typing import Literal

from pydantic import BaseModel, Field

class TutorResponse(BaseModel):

    message: str

    stage: Literal[
        "diagnose",
        "guiding_question",
        "hint",
        "feedback",
        "practice",
        "summary",
        "solution",
    ]

    student_understanding: Literal[
        "beginner",
        "developing",
        "intermediate",
        "advanced",
    ]

    answer_evaluation: Literal[
        "not_attempted",
        "correct",
        "partially_correct",
        "misconception",
        "incorrect",
        "unknown",
    ]

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    should_reveal_answer: bool
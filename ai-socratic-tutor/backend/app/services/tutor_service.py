from dataclasses import dataclass
from typing import Any

from app.services.fallback_service import FallbackTutorService


@dataclass
class TutorResponse:
    message: str
    stage: str
    action: str
    hint_level: int
    student_understanding: str
    answer_evaluation: str
    confidence: float
    should_reveal_answer: bool
    provider: str = "unknown"
    fallback_used: bool = False
    latency_ms: float = 0.0


def generate_tutor_response(
    message: str,
    history: list[dict],
    subject: str = "General",
) -> TutorResponse:

    fallback_service = FallbackTutorService()

    return fallback_service.generate_response(
        message=message,
        history=history,
        subject=subject,
    )
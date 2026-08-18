from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.session_state import session_manager

from app.services.tutor_service import (
    generate_tutor_response,
)

from app.services.decision_engine import (
    decide_next_action,
)


router = APIRouter(
    prefix="/api/tutor",
    tags=["Tutor"],
)


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = Field(default_factory=list)
    hint_level: int = 0
    session_id: str | None = None
    subject: str = "General"


class ChatResponse(BaseModel):
    message: str
    stage: str
    action: str
    hint_level: int
    student_understanding: str
    answer_evaluation: str
    confidence: float
    should_reveal_answer: bool

    # Provider monitoring
    provider: str
    fallback_used: bool
    latency_ms: float
    attempts: int
    solved: bool


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty.",
        )
    session = session_manager.get_session(request.session_id)

    try:

        # Generate response + provider metadata
        result = generate_tutor_response(
            message=request.message,
            history=request.history,
            subject=request.subject,
        )

        # Extract actual TutorResponse
        tutor_response = result.response

        # Decide next tutoring action
        decision = decide_next_action(
            evaluation=tutor_response.answer_evaluation,
            understanding=tutor_response.student_understanding,
            hint_level=session.current_hint_level,
            confidence=tutor_response.confidence,
        )
        updated_session= session_manager.update_session(
            session_id=request.session_id,
            evaluation=tutor_response.answer_evaluation,
            action=decision.action,
            hint_level=decision.hint_level,
        )

        return ChatResponse(
            message=tutor_response.message,

            stage=tutor_response.stage,

            action=decision.action,

            hint_level=decision.hint_level,

            student_understanding=(
                tutor_response.student_understanding
            ),

            answer_evaluation=(
                tutor_response.answer_evaluation
            ),

            confidence=tutor_response.confidence,

            should_reveal_answer=(
                tutor_response.should_reveal_answer
            ),

            # Provider monitoring
            provider=result.provider,

            fallback_used=result.fallback_used,

            latency_ms=round(
                result.latency_ms,
                2,
            ),
            attempts=updated_session.attempts,
            solved=updated_session.solved,
        )

    except Exception as exc:

        print(f"Tutor error: {exc}")

        raise HTTPException(
            status_code=500,
            detail="Unable to generate tutor response.",
        )

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session as DBSession

from app.database import get_db

from app.services.session_service import (
    add_message,
    complete_session,
    create_session,
    get_session,
)

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
@router.get("/test")
def test_tutor_router():
        return {
            "message": "Tutor router is working"
        }

class ChatRequest(BaseModel):
    message: str

    history: list[dict] = Field(
        default_factory=list
    )

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

    provider: str
    fallback_used: bool
    latency_ms: float

    attempts: int
    solved: bool


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    db: DBSession = Depends(get_db),
):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty.",
        )

    # --------------------------------------------------
    # 1. Make sure a session exists
    # --------------------------------------------------

    if not request.session_id:
        session = create_session(
            db=db,
            subject=request.subject,
            title=request.message[:50],
        )

    else:
        session = get_session(
            db=db,
            session_id=request.session_id,
        )

        if not session:
            raise HTTPException(
                status_code=404,
                detail="Session not found.",
            )

    # --------------------------------------------------
    # 2. Save student's message
    # --------------------------------------------------

    add_message(
        db=db,
        session_id=session.id,
        role="user",
        content=request.message,
        hint_level=request.hint_level,
    )

    try:

        # --------------------------------------------------
        # 3. Generate tutor response using existing service
        # --------------------------------------------------

        result = generate_tutor_response(
            message=request.message,
            history=request.history,
            subject=request.subject,
        )

        tutor_response = result

        # --------------------------------------------------
        # 4. Determine next tutoring action
        # --------------------------------------------------

        # Get current hint level from previous messages
        previous_messages = session.messages

        current_hint_level = 0

        for message in previous_messages:
            if message.role == "assistant":
                current_hint_level = max(
                    current_hint_level,
                    message.hint_level,
                )

        decision = decide_next_action(
            evaluation=tutor_response.answer_evaluation,
            understanding=tutor_response.student_understanding,
            hint_level=current_hint_level,
            confidence=tutor_response.confidence,
        )

        # --------------------------------------------------
        # 5. Save tutor response
        # --------------------------------------------------

        add_message(
            db=db,
            session_id=session.id,
            role="assistant",
            content=tutor_response.message,
            evaluation=tutor_response.answer_evaluation,
            understanding=tutor_response.student_understanding,
            confidence=tutor_response.confidence,
            hint_level=decision.hint_level,
            action=decision.action,
        )

        # --------------------------------------------------
        # 6. Check whether session is solved
        # --------------------------------------------------

        solved = (
            tutor_response.answer_evaluation.lower()
            == "correct"
        )

        if solved:
            complete_session(
                db=db,
                session_id=session.id,
            )

        # --------------------------------------------------
        # 7. Calculate attempts
        # --------------------------------------------------

        updated_messages = session.messages

        attempts = len(
            [
                message
                for message in updated_messages
                if message.role == "user"
            ]
        )

        # --------------------------------------------------
        # 8. Return response
        # --------------------------------------------------

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

            provider=result.provider,

            fallback_used=result.fallback_used,

            latency_ms=round(
                result.latency_ms,
                2,
            ),

            attempts=attempts,

            solved=solved,
        )

    except Exception as exc:

        print(
            f"Tutor error: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to generate tutor response.",
        )
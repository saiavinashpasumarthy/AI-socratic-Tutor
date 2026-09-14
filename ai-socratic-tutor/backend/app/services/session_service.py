from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session as DBSession

from app.models.session import Session
from app.models.message import Message


def create_session(
    db: DBSession,
    subject: str = "General",
    title: str = "New Session",
) -> Session:
    session = Session(
        id=str(uuid4()),
        title=title,
        subject=subject,
        status="active",
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_session(
    db: DBSession,
    session_id: str,
) -> Session | None:

    return (
        db.query(Session)
        .filter(Session.id == session_id)
        .first()
    )


def add_message(
    db: DBSession,
    session_id: str,
    role: str,
    content: str,
    evaluation: str | None = None,
    understanding: str | None = None,
    confidence: float | None = None,
    hint_level: int = 0,
    action: str | None = None,
) -> Message:

    message = Message(
        session_id=session_id,
        role=role,
        content=content,
        evaluation=evaluation,
        understanding=understanding,
        confidence=confidence,
        hint_level=hint_level,
        action=action,
    )

    db.add(message)

    # Update session activity
    session = get_session(db, session_id)

    if session:
        session.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(message)

    return message


def complete_session(
    db: DBSession,
    session_id: str,
) -> Session | None:

    session = get_session(db, session_id)

    if not session:
        return None

    session.status = "completed"
    session.completed_at = datetime.utcnow()
    session.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(session)

    return session


def get_session_messages(
    db: DBSession,
    session_id: str,
) -> list[Message]:

    return (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at.asc())
        .all()
    )


def delete_session(
    db: DBSession,
    session_id: str,
) -> bool:

    session = get_session(db, session_id)

    if not session:
        return False

    db.delete(session)
    db.commit()

    return True
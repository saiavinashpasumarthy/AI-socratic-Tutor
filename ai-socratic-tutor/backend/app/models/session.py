from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        default="New Session",
    )

    subject: Mapped[str] = mapped_column(
        String(100),
        default="General",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    messages = relationship(
        "Message",
        back_populates="session",
        cascade="all, delete-orphan",
    )
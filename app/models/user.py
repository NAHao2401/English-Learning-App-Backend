from datetime import datetime, date
from sqlalchemy import Date, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    current_level: Mapped[str] = mapped_column(String(50), default="Beginner")

    total_xp: Mapped[int] = mapped_column(Integer, default=0)

    streak_count: Mapped[int] = mapped_column(Integer, default=0)

    last_study_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    user_topics = relationship("UserTopic", back_populates="user", cascade="all, delete-orphan")
    saved_vocabularies = relationship("SavedVocabulary", back_populates="user", cascade="all, delete-orphan")

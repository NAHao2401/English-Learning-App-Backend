from datetime import datetime
from sqlalchemy import DateTime, Integer, String, func
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

    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)

    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    current_level: Mapped[str] = mapped_column(String(50), default="Beginner")

    total_xp: Mapped[int] = mapped_column(Integer, default=0)

    streak_count: Mapped[int] = mapped_column(Integer, default=0)

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
    user_vocabularies = relationship("UserVocabulary", back_populates="user", cascade="all, delete-orphan")
    device_tokens = relationship("DeviceToken", back_populates="user", cascade="all, delete-orphan")
    review_notification_state = relationship(
        "ReviewNotificationState",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )

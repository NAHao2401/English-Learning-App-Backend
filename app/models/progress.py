from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Progress(Base):
    __tablename__ = "progresses"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "lesson_id",
            name="uq_user_lesson_progress"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id"),
        nullable=False,
        index=True
    )

    status: Mapped[str] = mapped_column(String(20), default="not_started")

    completion_percent: Mapped[int] = mapped_column(Integer, default=0)

    highest_score: Mapped[int] = mapped_column(Integer, default=0)

    last_accessed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )


class XpHistory(Base):
    __tablename__ = "xp_histories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    lesson_id: Mapped[int | None] = mapped_column(
        ForeignKey("lessons.id"),
        nullable=True,
        index=True
    )

    source: Mapped[str] = mapped_column(String(50), nullable=False)

    xp_amount: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )


class ReviewHistory(Base):
    __tablename__ = "review_histories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    vocabulary_id: Mapped[int] = mapped_column(
        ForeignKey("vocabularies.id"),
        nullable=False,
        index=True,
    )

    result: Mapped[str] = mapped_column(String(20), nullable=False)

    reviewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )


class LessonSubmission(Base):
    __tablename__ = "lesson_submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id"),
        nullable=False,
        index=True
    )

    score: Mapped[int] = mapped_column(Integer, nullable=False)

    correct_count: Mapped[int] = mapped_column(Integer, nullable=False)

    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)

    xp_earned: Mapped[int] = mapped_column(Integer, default=0)

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )


class LessonAnswer(Base):
    __tablename__ = "lesson_answers"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "lesson_id",
            "question_id",
            name="uq_lesson_answers_user_lesson_question",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id"),
        nullable=False,
        index=True,
    )

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"),
        nullable=False,
        index=True,
    )

    answer: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)

    answered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    user = relationship("User")
    lesson = relationship("Lesson")
    question = relationship("Question")
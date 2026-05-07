from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserTopic(Base):
    __tablename__ = "user_topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="user_topics")
    saved_vocabularies = relationship("SavedVocabulary", back_populates="topic", cascade="all, delete-orphan")


class SavedVocabulary(Base):
    __tablename__ = "saved_vocabularies"
    __table_args__ = (
        UniqueConstraint("user_id", "vocabulary_id", name="uq_saved_vocabularies_user_vocab"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    vocabulary_id: Mapped[int] = mapped_column(ForeignKey("vocabularies.id"), nullable=False, index=True)
    user_topic_id: Mapped[int] = mapped_column(ForeignKey("user_topics.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="saved_vocabularies")
    vocabulary = relationship("Vocabulary", back_populates="saved_vocabularies")
    topic = relationship("UserTopic", back_populates="saved_vocabularies")
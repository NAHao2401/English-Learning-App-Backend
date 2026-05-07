from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Vocabulary(Base):
    __tablename__ = "vocabularies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"), nullable=False)
    word: Mapped[str] = mapped_column(String(150), nullable=False)
    meaning: Mapped[str | None] = mapped_column(Text, nullable=True)
    pronunciation: Mapped[str | None] = mapped_column(String(255), nullable=True)
    example_sentence: Mapped[str | None] = mapped_column(Text, nullable=True)
    audio_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    difficulty: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    topic = relationship("Topic", back_populates="vocabularies")
    saved_vocabularies = relationship("SavedVocabulary", back_populates="vocabulary", cascade="all, delete-orphan")

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class VocabularyResponse(BaseModel):
    id: int
    topic_id: int
    word: str
    meaning: str | None = None
    pronunciation: str | None = None
    example_sentence: str | None = None
    audio_url: str | None = None
    example_audio_url: str | None = None
    difficulty: str | None = None

    model_config = {"from_attributes": True}


class UserTopicCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None


class UserTopicResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: str | None = None

    model_config = {"from_attributes": True}


class SaveVocabularyRequest(BaseModel):
    vocabulary_id: int
    user_topic_id: int | None = None
    new_topic: UserTopicCreateRequest | None = None

    @model_validator(mode="after")
    def validate_topic_choice(self):
        has_existing_topic = self.user_topic_id is not None
        has_new_topic = self.new_topic is not None

        if has_existing_topic == has_new_topic:
            raise ValueError("Provide either user_topic_id or new_topic")

        return self


class SavedVocabularyResponse(BaseModel):
    id: int
    user_topic_id: int
    vocabulary_id: int
    topic: UserTopicResponse
    vocabulary: VocabularyResponse

    model_config = {"from_attributes": True}


class RateVocabRequest(BaseModel):
    vocabulary_id: int
    rating: int


class UserVocabularyResponse(BaseModel):
    id: int
    vocabulary_id: int
    is_saved: bool
    mastery_level: int
    last_reviewed_at: datetime | None
    review_count: int
    next_review_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class TopicStudyResponse(BaseModel):
    """Summary + word lists for study session."""

    topic_id: int
    total_words: int
    new_words: list[VocabularyResponse]
    due_review_words: list[VocabularyResponse]
    learned_count: int


class MasteryStatsResponse(BaseModel):
    """5 mastery level counts for the ring chart."""
    level_1: int = 0   # Chưa biết
    level_2: int = 0   # Mới học
    level_3: int = 0   # Nhớ tạm
    level_4: int = 0   # Nhớ lâu
    level_5: int = 0   # Thông thạo


class VocabOverviewResponse(BaseModel):
    """Summary card for VocabScreen — 'N từ đã học' block."""
    learned_count: int           # mastery_level >= 1
    due_review_count: int        # next_review_at <= now
    mastery_stats: MasteryStatsResponse


class LearnedVocabItem(BaseModel):
    """One learned word entry for LearnedWordsScreen."""
    vocabulary_id: int
    word: str
    meaning: str
    pronunciation: str | None
    audio_url: str | None = None
    example_audio_url: str | None = None
    example_sentence: str | None = None
    mastery_level: int
    review_count: int
    last_reviewed_at: datetime | None
    next_review_at: datetime | None    # computed
    is_due: bool                       # next_review_at <= now

    model_config = ConfigDict(from_attributes=True)


class LearnedVocabListResponse(BaseModel):
    items: list[LearnedVocabItem]
    total: int
    due_count: int                     # how many are due for review

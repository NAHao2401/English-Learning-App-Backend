from datetime import datetime

from pydantic import BaseModel, Field


# ---------- Request ----------

class SaveSpeakingPracticeRequest(BaseModel):
    target_text: str = Field(..., min_length=1)
    spoken_text: str | None = None
    score: int = Field(..., ge=0, le=100)
    is_matched: bool
    lesson_id: int | None = None


# ---------- Response ----------

class SpeakingPracticeResponse(BaseModel):
    id: int
    user_id: int
    lesson_id: int | None
    target_text: str
    spoken_text: str | None
    score: int
    is_matched: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class SpeakingStatsResponse(BaseModel):
    total_practices: int
    matched_count: int
    average_score: float
    best_score: int
    weekly_practices: list[int]   # 7 phần tử, index 0 = 6 ngày trước, index 6 = hôm nay


class SpeakingSentenceResponse(BaseModel):
    id: int
    sentence: str
    translation: str | None
    difficulty: str
    topic: str | None

    model_config = {"from_attributes": True}


class PaginatedPracticeResponse(BaseModel):
    items: list[SpeakingPracticeResponse]
    page: int
    limit: int
    total: int
    total_pages: int
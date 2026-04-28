from pydantic import BaseModel


class ProgressLessonResponse(BaseModel):
    lesson_id: int
    title: str
    status: str
    completion_percent: int
    highest_score: int
    is_locked: bool


class ProgressSummaryResponse(BaseModel):
    total_xp: int
    streak_count: int
    current_level: str
    completed_lessons: int
    total_lessons: int
    completion_percent: int
    study_days: int
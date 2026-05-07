from pydantic import BaseModel


class ProgressLessonResponse(BaseModel):
    lesson_id: int
    title: str
    status: str
    completion_percent: int
    highest_score: int
    is_locked: bool


class DailyXpResponse(BaseModel):
    date: str
    xp: int
    completed_lessons: int


class LessonStatusDistributionResponse(BaseModel):
    completed: int
    in_progress: int
    not_started: int
    locked: int


class LevelProgressResponse(BaseModel):
    current_level: str
    current_xp: int
    current_level_min_xp: int
    next_level: str | None = None
    next_level_min_xp: int | None = None
    progress_percent: int


class RecentActivityResponse(BaseModel):
    lesson_id: int
    lesson_title: str
    score: int
    xp_earned: int
    submitted_at: str


class ProgressSummaryResponse(BaseModel):
    total_xp: int
    streak_count: int
    current_level: str
    completed_lessons: int
    total_lessons: int
    completion_percent: int
    study_days: int

    in_progress_lessons: int = 0
    not_started_lessons: int = 0
    locked_lessons: int = 0

    total_submissions: int = 0
    average_score: int = 0
    best_score: int = 0

    remaining_lessons: int = 0
    lessons_chart: LessonStatusDistributionResponse
    weekly_xp: list[DailyXpResponse]
    level_progress: LevelProgressResponse
    recent_activities: list[RecentActivityResponse]
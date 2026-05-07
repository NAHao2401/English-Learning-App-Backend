from pydantic import BaseModel, Field


class TopicResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    icon_url: str | None = None
    level: str | None = None

    model_config = {"from_attributes": True}


class LessonResponse(BaseModel):
    id: int
    topic_id: int
    title: str
    description: str | None = None
    lesson_order: int | None = None
    difficulty: str | None = None
    estimated_time: int | None = None
    is_locked: bool = False
    completion_percent: int = 0
    status: str = "not_started"

    model_config = {"from_attributes": True}


class AnswerOptionResponse(BaseModel):
    id: int
    option_text: str
    option_order: int | None = None

    model_config = {"from_attributes": True}


class QuestionResponse(BaseModel):
    id: int
    lesson_id: int
    question_type: str  
    question_text: str
    audio_url: str | None = None
    explanation: str | None = None
    question_order: int | None = None
    answer_options: list[AnswerOptionResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class SubmitAnswerRequest(BaseModel):
    question_id: int
    answer: str = Field(min_length=1, max_length=500)


class SubmitLessonRequest(BaseModel):
    answers: list[SubmitAnswerRequest] = Field(min_length=1)


class SubmitLessonResponse(BaseModel):
    lesson_id: int
    total_questions: int
    correct_count: int
    wrong_count: int
    score: int
    xp_earned: int
    completion_percent: int
    passed: bool
    streak_count: int
    message: str
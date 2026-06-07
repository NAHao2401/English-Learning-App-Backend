from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.lesson import Lesson, Question, Topic
from app.models.speaking import SpeakingSentence
from app.models.user import User
from app.schemas.speaking import (
    PaginatedPracticeResponse,
    SaveSpeakingPracticeRequest,
    SpeakingPracticeResponse,
    SpeakingSentenceResponse,
    SpeakingStatsResponse,
)
from app.services import speaking_service

router = APIRouter(prefix="/speaking", tags=["Speaking"])


class SpeakingTopicResponse(BaseModel):
    id: int
    name: str
    sentence_count: int

    model_config = {"from_attributes": True}


class LessonSpeakingSentenceResponse(BaseModel):
    id: int
    text: str
    hint: str | None
    difficulty: str

    model_config = {"from_attributes": True}


class SpeakingResultRequest(BaseModel):
    question_id: int
    spoken_text: str
    score: int


def _get_speaking_topic_names(db: Session) -> list[str]:
    rows = (
        db.query(SpeakingSentence.topic, func.min(SpeakingSentence.id).label("first_id"))
        .filter(SpeakingSentence.topic.isnot(None))
        .group_by(SpeakingSentence.topic)
        .order_by(func.min(SpeakingSentence.id).asc())
        .all()
    )
    return [row[0] for row in rows]


@router.post("/practices", response_model=SpeakingPracticeResponse, status_code=201)
def save_practice(
    data: SaveSpeakingPracticeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Luu ket qua 1 lan luyen noi. Mobile goi sau khi tinh score xong."""
    return speaking_service.save_practice(db, current_user, data)


@router.get("/practices/me", response_model=PaginatedPracticeResponse)
def get_my_practices(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lay lich su luyen noi cua user hien tai, co phan trang."""
    return speaking_service.get_practices(db, current_user.id, page, limit)


@router.get("/practices/me/stats", response_model=SpeakingStatsResponse)
def get_my_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Thong ke tong hop cho Progress screen."""
    return speaking_service.get_stats(db, current_user.id)


@router.get("/sentences", response_model=list[SpeakingSentenceResponse])
def get_sentences(
    difficulty: str | None = Query(default=None, description="beginner / intermediate / advanced"),
    topic: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lay cau mau de luyen noi, loc theo difficulty va topic."""
    return speaking_service.get_sentences(db, difficulty, topic, limit)


@router.get("/topics", response_model=list[str])
def get_speaking_topics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lay danh sach topic co san trong bang speaking_sentences."""
    return _get_speaking_topic_names(db)


@router.get("/lesson-topics", response_model=list[SpeakingTopicResponse])
def get_lesson_speaking_topics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lay danh sach chu de lesson de luyen noi."""
    topics = db.query(Topic).all()
    result = []
    for topic in topics:
        count = (
            db.query(Question)
            .join(Lesson)
            .filter(Lesson.topic_id == topic.id)
            .count()
        )
        result.append(
            SpeakingTopicResponse(
                id=topic.id,
                name=topic.name,
                sentence_count=count,
            )
        )
    return result


@router.get("/topics/{topic_id}/sentences", response_model=list[SpeakingSentenceResponse])
def get_speaking_sentences_by_topic_id(
    topic_id: int,
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lay danh sach cau luyen noi theo thu tu topic trong bang speaking_sentences."""
    topics = _get_speaking_topic_names(db)
    if topic_id < 1 or topic_id > len(topics):
        raise HTTPException(status_code=404, detail="No speaking topic found")

    topic_name = topics[topic_id - 1]
    return (
        db.query(SpeakingSentence)
        .filter(SpeakingSentence.topic == topic_name)
        .order_by(SpeakingSentence.id.asc())
        .limit(limit)
        .all()
    )


@router.get("/lesson-topics/{topic_id}/sentences", response_model=list[LessonSpeakingSentenceResponse])
def get_lesson_sentences_by_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lay danh sach cau luyen noi theo chu de lesson."""
    questions = (
        db.query(Question)
        .join(Lesson)
        .filter(Lesson.topic_id == topic_id)
        .all()
    )
    if not questions:
        raise HTTPException(status_code=404, detail="No sentences found for this topic")

    return [
        LessonSpeakingSentenceResponse(
            id=question.id,
            text=question.question_text,
            hint=None,
            difficulty=question.lesson.difficulty or "beginner",
        )
        for question in questions
    ]


@router.post("/result")
def save_speaking_result(
    body: SpeakingResultRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Luu ket qua luyen noi cu va cong XP nho neu dat diem."""
    xp_earned = 5 if body.score >= 70 else 0
    if xp_earned:
        current_user.total_xp = (current_user.total_xp or 0) + xp_earned
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
    return {"message": "Saved", "xp_earned": xp_earned}

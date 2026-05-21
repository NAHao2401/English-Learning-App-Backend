<<<<<<< Updated upstream
# POST /speaking/practices
# Lưu kết quả 1 lần luyện nói (mobile gọi sau khi tính score xong)
{
  "target_text": "The quick brown fox",
  "spoken_text": "The quick brown dog",
  "score": 75,
  "is_matched": true,
  "lesson_id": null   # optional
}
=======
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Topic, Lesson, Question
from app.core.security import get_current_user
from app.models.models import User
from pydantic import BaseModel
from typing import List
>>>>>>> Stashed changes

router = APIRouter(prefix="/speaking", tags=["speaking"])


class SpeakingTopicResponse(BaseModel):
    id: int
    name: str
    sentence_count: int

    class Config:
        from_attributes = True


class SpeakingSentenceResponse(BaseModel):
    id: int
    text: str           # câu cần đọc
    hint: str | None    # gợi ý phát âm nếu có
    difficulty: str     # beginner / intermediate / advanced

    class Config:
        from_attributes = True


@router.get("/topics", response_model=List[SpeakingTopicResponse])
def get_speaking_topics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy danh sách chủ đề để luyện nói"""
    topics = db.query(Topic).all()
    result = []
    for topic in topics:
        # Đếm số câu speaking trong topic (dùng lại bảng Question)
        count = (
            db.query(Question)
            .join(Lesson)
            .filter(Lesson.topic_id == topic.id)
            .count()
        )
        result.append(SpeakingTopicResponse(
            id=topic.id,
            name=topic.name,
            sentence_count=count
        ))
    return result


@router.get("/topics/{topic_id}/sentences",
            response_model=List[SpeakingSentenceResponse])
def get_sentences_by_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy danh sách câu luyện nói theo chủ đề"""
    questions = (
        db.query(Question)
        .join(Lesson)
        .filter(Lesson.topic_id == topic_id)
        .all()
    )
    if not questions:
        raise HTTPException(status_code=404,
                            detail="No sentences found for this topic")

    return [
        SpeakingSentenceResponse(
            id=q.id,
            # Dùng lại trường question_text làm câu mẫu để đọc
            text=q.question_text,
            hint=None,
            difficulty=q.lesson.level if hasattr(q, 'lesson') else "beginner"
        )
        for q in questions
    ]


class SpeakingResultRequest(BaseModel):
    question_id: int
    spoken_text: str
    score: int


@router.post("/result")
def save_speaking_result(
    body: SpeakingResultRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lưu kết quả luyện nói (tích hợp XP nếu cần)"""
    # Cộng XP nhỏ mỗi lần luyện nói
    if body.score >= 70:
        current_user.total_xp = (current_user.total_xp or 0) + 5
        db.commit()
    return {"message": "Saved", "xp_earned": 5 if body.score >= 70 else 0}
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.lesson import TopicResponse
from app.schemas.vocabulary import (
    SaveVocabularyRequest,
    SavedVocabularyResponse,
    UserTopicCreateRequest,
    UserTopicResponse,
    VocabularyResponse,
)
from app.services.lesson_service import get_topics
from app.services.vocabulary_service import (
    create_user_topic,
    get_all_vocabularies,
    get_user_topic_vocabularies,
    get_user_topics,
    get_vocabularies_by_topic,
    remove_user_topic_vocabulary,
    save_vocabulary,
)

router = APIRouter(prefix="/vocabularies", tags=["Vocabularies"])


@router.get("/topics", response_model=list[TopicResponse])
def list_topics(db: Session = Depends(get_db)):
    return get_topics(db)


@router.get("/all", response_model=list[VocabularyResponse])
def list_vocabularies(level: str | None = None, db: Session = Depends(get_db)):
    return get_all_vocabularies(db, level)


@router.get("/topic/{topic_id}", response_model=list[VocabularyResponse])
def topic_vocabularies(topic_id: int, db: Session = Depends(get_db)):
    return get_vocabularies_by_topic(db, topic_id)


@router.get("/user-topics", response_model=list[UserTopicResponse])
def list_user_topics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_topics(db, current_user.id)


@router.post("/user-topics", response_model=UserTopicResponse, status_code=status.HTTP_201_CREATED)
def create_topic(
    request: UserTopicCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_user_topic(db, current_user.id, request.name, request.description)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/user-topics/{user_topic_id}/vocabularies", response_model=list[VocabularyResponse])
def list_user_topic_vocabularies(
    user_topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_topic_vocabularies(db, current_user.id, user_topic_id)


@router.delete("/user-topics/{user_topic_id}/vocabularies/{vocabulary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_topic_vocabulary(
    user_topic_id: int,
    vocabulary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        remove_user_topic_vocabulary(db, current_user.id, user_topic_id, vocabulary_id)
    except ValueError as exc:
        message = str(exc)
        if message in {"User topic not found", "Vocabulary is not saved in this topic"}:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


@router.post("/save", response_model=SavedVocabularyResponse, status_code=status.HTTP_201_CREATED)
def save_vocab_item(
    request: SaveVocabularyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return save_vocabulary(db, current_user.id, request)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

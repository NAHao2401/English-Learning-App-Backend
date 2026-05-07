from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user_vocabulary import SavedVocabulary, UserTopic
from app.models.vocabulary import Vocabulary
from app.schemas.vocabulary import SaveVocabularyRequest


def get_vocabularies_by_topic(db: Session, topic_id: int):
    return (
        db.query(Vocabulary)
        .filter(Vocabulary.topic_id == topic_id)
        .order_by(Vocabulary.id.asc())
        .all()
    )


def get_all_vocabularies(db: Session, level: str | None = None):
    query = db.query(Vocabulary)
    if level:
        query = query.filter(Vocabulary.difficulty == level)
    return query.order_by(Vocabulary.id.asc()).all()


def get_user_topics(db: Session, user_id: int):
    return (
        db.query(UserTopic)
        .filter(UserTopic.user_id == user_id)
        .order_by(UserTopic.id.asc())
        .all()
    )


def create_user_topic(db: Session, user_id: int, name: str, description: str | None = None):
    topic = UserTopic(user_id=user_id, name=name.strip(), description=description)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


def get_user_topic_vocabularies(db: Session, user_id: int, user_topic_id: int):
    return (
        db.query(Vocabulary)
        .join(SavedVocabulary, SavedVocabulary.vocabulary_id == Vocabulary.id)
        .join(UserTopic, UserTopic.id == SavedVocabulary.user_topic_id)
        .filter(
            UserTopic.id == user_topic_id,
            UserTopic.user_id == user_id,
            SavedVocabulary.user_id == user_id,
        )
        .order_by(Vocabulary.id.asc())
        .all()
    )


def save_vocabulary(db: Session, user_id: int, request: SaveVocabularyRequest):
    vocabulary = db.query(Vocabulary).filter(Vocabulary.id == request.vocabulary_id).first()
    if vocabulary is None:
        raise ValueError("Vocabulary not found")

    if request.user_topic_id is not None:
        user_topic = (
            db.query(UserTopic)
            .filter(UserTopic.id == request.user_topic_id, UserTopic.user_id == user_id)
            .first()
        )
        if user_topic is None:
            raise ValueError("User topic not found")
    else:
        if request.new_topic is None:
            raise ValueError("Provide either user_topic_id or new_topic")
        user_topic = create_user_topic(db, user_id, request.new_topic.name, request.new_topic.description)

    saved_vocabulary = (
        db.query(SavedVocabulary)
        .filter(
            SavedVocabulary.user_id == user_id,
            SavedVocabulary.vocabulary_id == request.vocabulary_id,
        )
        .first()
    )

    try:
        if saved_vocabulary is None:
            saved_vocabulary = SavedVocabulary(
                user_id=user_id,
                vocabulary_id=request.vocabulary_id,
                user_topic_id=user_topic.id,
            )
            db.add(saved_vocabulary)
        else:
            saved_vocabulary.user_topic_id = user_topic.id

        db.commit()
        db.refresh(saved_vocabulary)
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("Unable to save vocabulary") from exc

    return saved_vocabulary


def remove_user_topic_vocabulary(db: Session, user_id: int, user_topic_id: int, vocabulary_id: int):
    user_topic = (
        db.query(UserTopic)
        .filter(UserTopic.id == user_topic_id, UserTopic.user_id == user_id)
        .first()
    )
    if user_topic is None:
        raise ValueError("User topic not found")

    saved_vocabulary = (
        db.query(SavedVocabulary)
        .filter(
            SavedVocabulary.user_id == user_id,
            SavedVocabulary.user_topic_id == user_topic_id,
            SavedVocabulary.vocabulary_id == vocabulary_id,
        )
        .first()
    )
    if saved_vocabulary is None:
        raise ValueError("Vocabulary is not saved in this topic")

    db.delete(saved_vocabulary)
    db.commit()

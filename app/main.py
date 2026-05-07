from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.lesson import router as lesson_router
from app.api.progress import router as progress_router
from app.api.vocabulary import router as vocabulary_router
from app.db.base import Base
from app.db.session import engine
from app.models.user import User
from app.models.user_vocabulary import SavedVocabulary, UserTopic
from app.models.vocabulary import Vocabulary
from app.models.lesson import Lesson, Question, AnswerOption, Topic
from app.models.progress import Progress, XpHistory

Base.metadata.create_all(bind=engine)

app = FastAPI(title="English Learning App API")

app.include_router(auth_router)
app.include_router(vocabulary_router)
app.include_router(lesson_router)
app.include_router(progress_router)

@app.get("/")
def root():
    return {"message": "API is running"}
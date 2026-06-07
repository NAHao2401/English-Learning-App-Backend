from app.db.session import SessionLocal
from app.models.lesson import Topic
from app.models.speaking import SpeakingSentence

if __name__ == '__main__':
    db = SessionLocal()
    try:
        topics = db.query(Topic).order_by(Topic.id).all()
        if not topics:
            print('No topics found')
        for t in topics:
            c = db.query(SpeakingSentence).filter(SpeakingSentence.topic == t.name).count()
            print(t.id, t.name, c)
    finally:
        db.close()

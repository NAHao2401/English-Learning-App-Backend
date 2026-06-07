from app.db.session import SessionLocal
from app.models.lesson import Topic
from app.models.speaking import SpeakingSentence
from sqlalchemy import func

if __name__ == '__main__':
    db = SessionLocal()
    try:
        topics = db.query(Topic).order_by(Topic.id).all()
        if not topics:
            print('No topics found')
        for t in topics:
            print('--- Topic', t.id, t.name)
            sentences = db.query(SpeakingSentence).filter(func.lower(SpeakingSentence.topic) == func.lower(t.name)).limit(5).all()
            print('found', db.query(SpeakingSentence).filter(func.lower(SpeakingSentence.topic) == func.lower(t.name)).count(), 'sentences')
            for s in sentences:
                print('id:', getattr(s, 'id', None))
                print('sentence attr:', getattr(s, 'sentence', None))
                print('translation attr:', getattr(s, 'translation', None))
                print('difficulty attr:', getattr(s, 'difficulty', None))
                print('topic attr:', getattr(s, 'topic', None))
                print('repr:', repr(s))
                print('dict:', {k: v for k, v in s.__dict__.items() if not k.startswith('_')})
                print('---')
    finally:
        db.close()

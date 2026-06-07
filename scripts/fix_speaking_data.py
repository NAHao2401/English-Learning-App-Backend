"""
Fill missing fields in speaking_sentences and normalize topic names to existing Topic.name.
Run:
    .\.venv\Scripts\python.exe scripts\fix_speaking_data.py
"""
from app.db.session import SessionLocal
from app.models.speaking import SpeakingSentence
from app.models.lesson import Topic


def normalize_topic(s, topic_map, default_topic):
    if s.topic:
        key = s.topic.strip().lower()
        if key in topic_map:
            return topic_map[key]
        # try contains
        for k, v in topic_map.items():
            if k in key:
                return v
    return default_topic


def main():
    db = SessionLocal()
    try:
        topics = db.query(Topic).order_by(Topic.id).all()
        if not topics:
            print('No topics found; aborting')
            return
        topic_map = {t.name.strip().lower(): t.name for t in topics}
        default_topic = topics[0].name

        total = db.query(SpeakingSentence).count()
        print('Total speaking sentences:', total)
        updated = 0

        for s in db.query(SpeakingSentence).all():
            changed = False
            if s.sentence is None or (isinstance(s.sentence, str) and s.sentence.strip() == ''):
                s.sentence = f"Practice sentence {s.id or 'new'}"
                changed = True
            if s.translation is None:
                s.translation = ''
                changed = True
            if s.difficulty is None or (isinstance(s.difficulty, str) and s.difficulty.strip() == ''):
                s.difficulty = 'beginner'
                changed = True
            new_topic = normalize_topic(s, topic_map, default_topic)
            if s.topic != new_topic:
                s.topic = new_topic
                changed = True
            if changed:
                db.add(s)
                updated += 1

        db.commit()
        print('Updated rows:', updated)

        # print 10 sample rows
        rows = db.query(SpeakingSentence).limit(10).all()
        for r in rows:
            print({'id': r.id, 'sentence': r.sentence, 'translation': r.translation, 'difficulty': r.difficulty, 'topic': r.topic})

    finally:
        db.close()


if __name__ == '__main__':
    main()

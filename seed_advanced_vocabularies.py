from app.db.session import SessionLocal, engine
from app.models.lesson import Topic
from app.models.vocabulary import Vocabulary
from advanced_vocab_topics import ADVANCED_VOCAB_TOPICS, audio_slug


def seed_advanced_vocabularies() -> None:
    engine.echo = False
    db = SessionLocal()
    try:
        created_topics = 0
        updated_topics = 0
        created_vocabularies = 0
        updated_vocabularies = 0

        for topic_data in ADVANCED_VOCAB_TOPICS:
            topic_names = [topic_data["name"], *topic_data.get("legacy_names", [])]
            topic = db.query(Topic).filter(Topic.name.in_(topic_names)).first()
            if topic is None:
                topic = Topic(
                    name=topic_data["name"],
                    description=topic_data["description"],
                    icon_url=topic_data["icon_url"],
                    level=topic_data["level"],
                )
                db.add(topic)
                db.commit()
                db.refresh(topic)
                created_topics += 1
            else:
                topic.name = topic_data["name"]
                topic.description = topic_data["description"]
                topic.icon_url = topic_data["icon_url"]
                topic.level = topic_data["level"]
                updated_topics += 1

            for item in topic_data["vocabularies"]:
                slug = audio_slug(item["word"])
                audio_url = f"static/audio/words/{slug}.mp3"
                example_audio_url = f"static/audio/examples/{slug}_example.mp3"
                vocabulary = (
                    db.query(Vocabulary)
                    .filter(
                        Vocabulary.topic_id == topic.id,
                        Vocabulary.word == item["word"],
                    )
                    .first()
                )

                if vocabulary is None:
                    db.add(
                        Vocabulary(
                            topic_id=topic.id,
                            word=item["word"],
                            meaning=item["meaning"],
                            pronunciation=item["pronunciation"],
                            example_sentence=item["example_sentence"],
                            audio_url=audio_url,
                            example_audio_url=example_audio_url,
                            difficulty=topic_data["level"],
                        )
                    )
                    created_vocabularies += 1
                else:
                    vocabulary.meaning = item["meaning"]
                    vocabulary.pronunciation = item["pronunciation"]
                    vocabulary.example_sentence = item["example_sentence"]
                    vocabulary.audio_url = audio_url
                    vocabulary.example_audio_url = example_audio_url
                    vocabulary.difficulty = topic_data["level"]
                    updated_vocabularies += 1

            db.commit()

        print("Advanced vocabulary database update completed.")
        print(f"   - Topics created: {created_topics}")
        print(f"   - Topics updated: {updated_topics}")
        print(f"   - Vocabularies created: {created_vocabularies}")
        print(f"   - Vocabularies updated: {updated_vocabularies}")
    except Exception as exc:
        db.rollback()
        print(f"Error updating advanced vocabulary data: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_advanced_vocabularies()

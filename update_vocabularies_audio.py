"""
Script to update existing vocabulary records with audio URLs
"""
import re
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.vocabulary import Vocabulary

def extract_audio_urls():
    """Extract audio URLs from seed_vocabularies.py"""
    with open('seed_vocabularies.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    audio_mapping = {}
    
    # Find all Vocabulary entries
    pattern = r'Vocabulary\(([^)]+)\)'
    matches = re.findall(pattern, content)
    
    for vocab_params in matches:
        word_match = re.search(r'word="([^"]+)"', vocab_params)
        audio_match = re.search(r'audio_url="([^"]+)"', vocab_params)
        example_audio_match = re.search(r'example_audio_url="([^"]+)"', vocab_params)
        
        if word_match:
            word = word_match.group(1)
            audio_url = audio_match.group(1) if audio_match else None
            example_audio_url = example_audio_match.group(1) if example_audio_match else None
            audio_mapping[word] = {
                'audio_url': audio_url,
                'example_audio_url': example_audio_url
            }
    
    return audio_mapping

def update_vocabularies():
    """Update existing vocabulary records with audio URLs"""
    db = SessionLocal()
    try:
        audio_mapping = extract_audio_urls()
        updated_count = 0
        
        for word, urls in audio_mapping.items():
            vocab = db.query(Vocabulary).filter(Vocabulary.word == word).first()
            if vocab:
                vocab.audio_url = urls['audio_url']
                vocab.example_audio_url = urls['example_audio_url']
                updated_count += 1
        
        db.commit()
        print(f"✅ Updated {updated_count} vocabulary records with audio URLs")
        
    except Exception as e:
        print(f"❌ Update failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_vocabularies()

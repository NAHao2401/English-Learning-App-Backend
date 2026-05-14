"""
Script to add example_audio_url column to vocabularies table
"""
from sqlalchemy import text
from app.db.session import engine

def migrate():
    with engine.connect() as connection:
        try:
            # Add example_audio_url column if it doesn't exist
            connection.execute(text("""
                ALTER TABLE vocabularies 
                ADD COLUMN IF NOT EXISTS example_audio_url VARCHAR(255) NULL
            """))
            connection.commit()
            print("✅ Migration complete: Added example_audio_url column to vocabularies table")
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            connection.rollback()

if __name__ == "__main__":
    migrate()

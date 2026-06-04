"""Add FCM device tokens and persisted vocabulary review due times."""

from sqlalchemy import text

from app.db.session import engine


def migrate() -> None:
    statements = [
        """
        ALTER TABLE user_vocabularies
        ADD COLUMN IF NOT EXISTS next_review_at TIMESTAMPTZ NULL
        """,
        """
        UPDATE user_vocabularies
        SET next_review_at = last_reviewed_at + (
            CASE mastery_level
                WHEN 0 THEN INTERVAL '0 days'
                WHEN 1 THEN INTERVAL '1 day'
                WHEN 2 THEN INTERVAL '2 days'
                WHEN 3 THEN INTERVAL '4 days'
                WHEN 4 THEN INTERVAL '8 days'
                WHEN 5 THEN INTERVAL '16 days'
                ELSE INTERVAL '1 day'
            END
        )
        WHERE last_reviewed_at IS NOT NULL
          AND next_review_at IS NULL
        """,
        """
        CREATE INDEX IF NOT EXISTS ix_user_vocabularies_next_review_at
        ON user_vocabularies (next_review_at)
        """,
        """
        CREATE TABLE IF NOT EXISTS device_tokens (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            token TEXT NOT NULL UNIQUE,
            platform VARCHAR(20) NOT NULL DEFAULT 'android',
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
        """,
        """
        CREATE INDEX IF NOT EXISTS ix_device_tokens_user_id
        ON device_tokens (user_id)
        """,
        """
        ALTER TABLE device_tokens
        DROP COLUMN IF EXISTS last_review_signature
        """,
        """
        CREATE TABLE IF NOT EXISTS review_notification_states (
            user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
            last_review_activity_at TIMESTAMPTZ NULL,
            last_review_signature VARCHAR(64) NULL,
            last_notified_at TIMESTAMPTZ NULL
        )
        """,
        """
        INSERT INTO review_notification_states (user_id, last_review_activity_at)
        SELECT user_id, MAX(reviewed_at)
        FROM review_histories
        GROUP BY user_id
        ON CONFLICT (user_id) DO UPDATE SET
            last_review_activity_at = GREATEST(
                review_notification_states.last_review_activity_at,
                EXCLUDED.last_review_activity_at
            )
        """,
    ]

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))

    print("Migration complete: added FCM notification tables and review due times")


if __name__ == "__main__":
    migrate()

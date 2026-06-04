import unittest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import patch

from firebase_admin import messaging

from app.jobs import review_notifications
from app.models.device_token import DeviceToken
from app.models.review_notification_state import ReviewNotificationState


class FakeQuery:
    def __init__(self, rows):
        self.rows = rows

    def filter(self, *args):
        return self

    def order_by(self, *args):
        return self

    def all(self):
        return self.rows


class FakeDb:
    def __init__(self, tokens, states):
        self.tokens = tokens
        self.states = states
        self.added = []
        self.deleted = []
        self.committed = False

    def execute(self, statement):
        return SimpleNamespace(scalar_one=lambda: True)

    def query(self, model):
        if model is DeviceToken:
            return FakeQuery(self.tokens)
        if model is ReviewNotificationState:
            return FakeQuery(self.states)
        raise AssertionError(f"Unexpected query model: {model}")

    def add(self, item):
        self.added.append(item)

    def delete(self, item):
        self.deleted.append(item)

    def commit(self):
        self.committed = True


class ReviewNotificationJobTests(unittest.TestCase):
    def test_recent_review_activity_skips_notification(self):
        token = DeviceToken(id=1, user_id=7, token="token-1", platform="android")
        state = ReviewNotificationState(
            user_id=7,
            last_review_activity_at=datetime.now(timezone.utc),
        )
        db = FakeDb(tokens=[token], states=[state])

        with (
            patch.object(review_notifications, "_get_due_vocabularies_by_user", return_value={7: [1, 2]}),
            patch.object(review_notifications, "_initialize_firebase"),
            patch.object(review_notifications, "_send_review_reminder") as send,
        ):
            review_notifications.send_due_review_notifications(db)

        send.assert_not_called()

    def test_ten_due_words_send_only_one_notification_per_user(self):
        tokens = [
            DeviceToken(id=1, user_id=7, token="newest-token", platform="android"),
            DeviceToken(id=2, user_id=7, token="older-token", platform="android"),
        ]
        db = FakeDb(tokens=tokens, states=[])
        due_ids = list(range(1, 11))

        with (
            patch.object(review_notifications, "_get_due_vocabularies_by_user", return_value={7: due_ids}),
            patch.object(review_notifications, "_initialize_firebase"),
            patch.object(review_notifications, "_send_review_reminder") as send,
        ):
            review_notifications.send_due_review_notifications(db)

        send.assert_called_once_with("newest-token", 10)
        self.assertEqual(len(db.added), 1)
        self.assertEqual(db.added[0].last_review_signature, review_notifications._build_signature(due_ids))

    def test_unregistered_token_is_deleted_before_trying_next_token(self):
        tokens = [
            DeviceToken(id=1, user_id=7, token="invalid-token", platform="android"),
            DeviceToken(id=2, user_id=7, token="valid-token", platform="android"),
        ]
        db = FakeDb(tokens=tokens, states=[])

        def send(token, due_count):
            if token == "invalid-token":
                raise messaging.UnregisteredError("gone")

        with (
            patch.object(review_notifications, "_get_due_vocabularies_by_user", return_value={7: [1, 2]}),
            patch.object(review_notifications, "_initialize_firebase"),
            patch.object(review_notifications, "_send_review_reminder", side_effect=send) as send_mock,
        ):
            review_notifications.send_due_review_notifications(db)

        self.assertEqual(send_mock.call_count, 2)
        self.assertEqual(db.deleted, [tokens[0]])
        self.assertEqual(len(db.added), 1)

    def test_signature_only_uses_current_due_vocabulary_ids(self):
        signature = review_notifications._build_signature([1, 2, 3])

        self.assertEqual(signature, review_notifications._build_signature([1, 2, 3]))
        self.assertNotEqual(signature, review_notifications._build_signature([1, 2]))


if __name__ == "__main__":
    unittest.main()

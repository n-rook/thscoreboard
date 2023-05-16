from collections.abc import Callable
from typing import Any
from django.db import connections, transaction
from django.test import Client
from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

from replays.testing import test_replays
from replays.testing.test_case import ReplayTestCase
import users.models as user_models
import replays.models as replay_models


CONFIRM_BUTTON_HTML = (
    '<input type="submit" name="submit" value="Confirm" class="spaced-input">'
)
DELETE_BUTTON_HTML = (
    '<input type="submit" name="submit" value="Delete request" class="spaced-input">'
)
APPROVE_BUTTON_HTML = (
    '<input type="submit" name="submit" value="Approve" class="spaced-input">'
)
CHECKBOX_HIDDEN_HTML = "hidden\n"
READONLY_CONTACT_INFO_HTML = '<input type="text" name="contact_info" value="contact info" maxlength="200" readonly="readonly" required id="id_contact_info">'


class ReviewClaimTest(ReplayTestCase):
    def setUp(self):
        self.user = self.createUser("user")
        self.staff_user = self.createUser("staff_user")
        self.staff_user.is_staff = True
        self.staff_user.save()
        self.other_user = self.createUser("user2")
        super().setUp()

    @classmethod
    def tearDownClass(cls):
        # Force database connections to close - see https://stackoverflow.com/a/63176624
        cursor = connection.cursor()
        database_name = "test_thscoreboard"
        cursor.execute(
            "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity "
            "WHERE pg_stat_activity.datname = %s AND pid <> pg_backend_pid();",
            [database_name],
        )
        super().tearDownClass()

    def test_user_reviews_their_request(self) -> None:
        self.client.force_login(self.user)
        claim_replay_request = self._create_claim_replay_request(self.user)

        response = self.client.get(f"/users/claim/{claim_replay_request.id}")

        self.assertContains(response, DELETE_BUTTON_HTML)
        self.assertContains(response, READONLY_CONTACT_INFO_HTML)
        self.assertNotContains(response, CONFIRM_BUTTON_HTML)
        self.assertNotContains(response, APPROVE_BUTTON_HTML)
        self.assertContains(response, CHECKBOX_HIDDEN_HTML)

    def test_user_deletes_their_request(self) -> None:
        self.client.force_login(self.user)
        claim_replay_request = self._create_claim_replay_request(self.user)

        response = self.client.post(
            f"/users/claim/{claim_replay_request.id}",
            {
                "silentselene_username": [self.user.get_username()],
                "contact_info": ["contact info"],
                "choices": [claim_replay_request.replays.get().id],
                "submit": ["Delete request"],
            },
        )

        self.assertContains(response, "Success!")
        claim_replay_request = user_models.ClaimReplayRequest.objects.first()
        self.assertEqual(
            claim_replay_request.request_status, user_models.RequestStatus.USER_DELETED
        )

    def test_staff_reviews_request(self) -> None:
        self.client.force_login(self.staff_user)
        claim_replay_request = self._create_claim_replay_request(self.user)

        response = self.client.get(f"/users/claim/{claim_replay_request.id}")

        self.assertContains(response, DELETE_BUTTON_HTML)
        self.assertContains(response, READONLY_CONTACT_INFO_HTML)
        self.assertNotContains(response, CONFIRM_BUTTON_HTML)
        self.assertContains(response, APPROVE_BUTTON_HTML)
        self.assertNotContains(response, CHECKBOX_HIDDEN_HTML)

    def test_staff_deletes_request(self) -> None:
        self.client.force_login(self.staff_user)
        claim_replay_request = self._create_claim_replay_request(self.user)

        response = self.client.post(
            f"/users/claim/{claim_replay_request.id}",
            {
                "silentselene_username": [self.user.get_username()],
                "contact_info": ["contact info"],
                "choices": [claim_replay_request.replays.get().id],
                "submit": ["Delete request"],
            },
        )

        self.assertContains(response, "Success!")
        claim_replay_request = user_models.ClaimReplayRequest.objects.first()
        self.assertEqual(
            claim_replay_request.request_status, user_models.RequestStatus.STAFF_DELETED
        )

    def test_staff_approves_request(self) -> None:
        self.client.force_login(self.staff_user)
        claim_replay_request = self._create_claim_replay_request(self.user)

        response = self.client.post(
            f"/users/claim/{claim_replay_request.id}",
            {
                "silentselene_username": [self.user.get_username()],
                "contact_info": ["contact info"],
                "choices": [claim_replay_request.replays.get().id],
                "submit": ["Approve"],
            },
        )

        self.assertContains(response, "Success!")
        claim_replay_request = user_models.ClaimReplayRequest.objects.first()
        self.assertEqual(
            claim_replay_request.request_status, user_models.RequestStatus.APPROVED
        )
        replay = claim_replay_request.replays.get()
        self.assertAlmostEqual(replay.user, self.user)

    def test_user_cannot_review_other_users_claim(self) -> None:
        self.client.force_login(self.user)
        claim_replay_request = self._create_claim_replay_request(self.other_user)

        with self.assertLogs():
            response = self.client.get(f"/users/claim/{claim_replay_request.id}")
            self.assertEqual(response.status_code, 403)

    def test_user_cannot_review_deleted_claim(self) -> None:
        self.client.force_login(self.user)
        claim_replay_request = self._create_claim_replay_request(self.user)
        claim_replay_request.request_status = user_models.RequestStatus.USER_DELETED
        claim_replay_request.save()

        with self.assertLogs():
            response = self.client.get(f"/users/claim/{claim_replay_request.id}")
            self.assertEqual(response.status_code, 403)

    def _create_claim_replay_request(
        self, request_owner
    ) -> user_models.ClaimReplayRequest:
        replay = test_replays.CreateAsPublishedReplay("th6_hard_1cc", request_owner)
        claim_replay_request = user_models.ClaimReplayRequest.objects.create(
            user=request_owner,
            contact_info="contact info",
            request_status=user_models.RequestStatus.SUBMITTED,
        )
        claim_replay_request.save()
        claim_replay_request.replays.set([replay])
        return claim_replay_request

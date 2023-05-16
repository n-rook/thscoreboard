from django.db import connection

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
CHECKBOX_HTML = "checkbox"
HIDDEN_CHECKBOX_HTML = "hidden\n"
READONLY_CONTACT_INFO_HTML = '<input type="text" name="contact_info" value="contact info" maxlength="200" readonly="readonly" required id="id_contact_info">'
READONLY_CONTACT_INFO_WITH_PLACEHOLDER_HTML = '<input type="text" name="contact_info" value="Not applicable" maxlength="200" readonly="readonly" required id="id_contact_info">'
CONTACT_INFO_HTML = '<input type="text" name="contact_info" maxlength="200" required id="id_contact_info">'


class ClaimReplaysTest(ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.createUser("user")
        self.staff_user = self.createUser("staff_user", is_staff=True)
        self.replay = test_replays.CreateAsPublishedReplay(
            "th6_hard_1cc", imported_username="imported"
        )

    @classmethod
    def tearDownClass(cls):
        _force_close_all_database_connections()
        super().tearDownClass()

    def test_user_views_request_page(self) -> None:
        self.client.force_login(self.user)

        response = self.client.post(
            "/users/claim",
            {
                "silentselene_username": [self.user.get_username()],
                "royalflare_username": [self.replay.imported_username],
            },
        )

        self.assertNotContains(response, DELETE_BUTTON_HTML)
        self.assertContains(response, CONTACT_INFO_HTML)
        self.assertContains(response, CONFIRM_BUTTON_HTML)
        self.assertNotContains(response, APPROVE_BUTTON_HTML)
        self.assertContains(response, CHECKBOX_HTML)

    def test_user_creates_claim_request(self) -> None:
        self.client.force_login(self.user)

        response = self.client.post(
            "/users/claim",
            {
                "silentselene_username": [self.user.get_username()],
                "contact_info": ["contact info"],
                "choices": [self.replay.id],
                "submit": ["Confirm"],
            },
        )

        self.assertContains(response, "Success!")
        claim_replay_request = user_models.ClaimReplayRequest.objects.first()
        self.assertEqual(claim_replay_request.user, self.user)
        self.assertEqual(claim_replay_request.contact_info, "contact info")
        self.assertEqual(
            claim_replay_request.request_status, user_models.RequestStatus.SUBMITTED
        )

    def test_staff_views_request_page(self) -> None:
        self.client.force_login(self.staff_user)

        response = self.client.post(
            "/users/claim",
            {
                "silentselene_username": [self.user.get_username()],
                "royalflare_username": [self.replay.imported_username],
            },
        )

        print(response.content)

        self.assertNotContains(response, DELETE_BUTTON_HTML)
        self.assertContains(response, READONLY_CONTACT_INFO_WITH_PLACEHOLDER_HTML)
        self.assertNotContains(response, CONFIRM_BUTTON_HTML)
        self.assertContains(response, APPROVE_BUTTON_HTML)
        self.assertContains(response, CHECKBOX_HTML)

    def test_staff_creates_claims(self) -> None:
        self.client.force_login(self.staff_user)

        response = self.client.post(
            "/users/claim",
            {
                "silentselene_username": [self.user.get_username()],
                "contact_info": ["contact info"],
                "choices": [self.replay.id],
                "submit": ["Confirm"],
            },
        )

        self.assertContains(response, "Success!")
        self.assertEqual(user_models.ClaimReplayRequest.objects.count(), 0)
        replay = replay_models.Replay.objects.first()
        self.assertEqual(replay.user, self.user)


class ReviewClaimReplaysTest(ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.createUser("user")
        self.staff_user = self.createUser("staff_user", is_staff=True)
        self.other_user = self.createUser("user2")

    @classmethod
    def tearDownClass(cls):
        _force_close_all_database_connections()
        super().tearDownClass()

    def test_user_reviews_their_claim_request(self) -> None:
        self.client.force_login(self.user)
        claim_replay_request = self._create_claim_replay_request(self.user)

        response = self.client.get(f"/users/claim/{claim_replay_request.id}")

        self.assertContains(response, DELETE_BUTTON_HTML)
        self.assertContains(response, READONLY_CONTACT_INFO_HTML)
        self.assertNotContains(response, CONFIRM_BUTTON_HTML)
        self.assertNotContains(response, APPROVE_BUTTON_HTML)
        self.assertContains(response, HIDDEN_CHECKBOX_HTML)

    def test_user_deletes_their_claim_request(self) -> None:
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

    def test_staff_reviews_claim_request(self) -> None:
        self.client.force_login(self.staff_user)
        claim_replay_request = self._create_claim_replay_request(self.user)

        response = self.client.get(f"/users/claim/{claim_replay_request.id}")

        print(response.content)

        self.assertContains(response, DELETE_BUTTON_HTML)
        self.assertContains(response, READONLY_CONTACT_INFO_HTML)
        self.assertNotContains(response, CONFIRM_BUTTON_HTML)
        self.assertContains(response, APPROVE_BUTTON_HTML)
        self.assertNotContains(response, HIDDEN_CHECKBOX_HTML)

    def test_staff_deletes_claim_request(self) -> None:
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

    def test_staff_approves_claim_request(self) -> None:
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
        self.assertEqual(replay.user, self.user)

    def test_user_cannot_review_other_users_claim_request(self) -> None:
        self.client.force_login(self.user)
        claim_replay_request = self._create_claim_replay_request(self.other_user)

        with self.assertLogs():
            response = self.client.get(f"/users/claim/{claim_replay_request.id}")
            self.assertEqual(response.status_code, 403)

    def test_user_cannot_review_deleted_claim_request(self) -> None:
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
        replay = test_replays.CreateAsPublishedReplay(
            "th6_hard_1cc", imported_username="imported"
        )
        claim_replay_request = user_models.ClaimReplayRequest.objects.create(
            user=request_owner,
            contact_info="contact info",
            request_status=user_models.RequestStatus.SUBMITTED,
        )
        claim_replay_request.save()
        claim_replay_request.replays.set([replay])
        return claim_replay_request


def _force_close_all_database_connections() -> None:
    # See https://stackoverflow.com/a/63176624
    cursor = connection.cursor()
    database_name = "test_thscoreboard"
    cursor.execute(
        "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity "
        "WHERE pg_stat_activity.datname = %s AND pid <> pg_backend_pid();",
        [database_name],
    )

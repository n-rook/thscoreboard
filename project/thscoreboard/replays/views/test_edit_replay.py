from django.template import response as template_response
from django import test as django_test
from django import urls

from replays import models
from replays.views import edit_replay
from replays.testing import test_case
from replays.testing import test_replays


def _Url(game_id, replay_id):
    return urls.reverse(
        "edit_replay", kwargs={"game_id": game_id, "replay_id": replay_id}
    )


class EditReplayTestCase(test_case.ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.factory = django_test.RequestFactory()
        self.user = self.createUser("some-user")

    def _Get(self, game_id, replay_id):
        request = self.factory.get(_Url(game_id, replay_id))
        request.user = self.user
        return edit_replay.edit_replay(request, game_id=game_id, replay_id=replay_id)

    def _Post(self, game_id, replay_id, data):
        request = self.factory.post(_Url(game_id, replay_id), data=data)
        request.user = self.user
        return edit_replay.edit_replay(request, game_id=game_id, replay_id=replay_id)

    def testWrongUserCannotViewEditScreen(self):
        other_user = self.createUser("bob")
        r = test_replays.CreateAsPublishedReplay("th10_normal", other_user)

        response = self._Get(r.shot.game.game_id, r.id)
        self.assertEqual(response.status_code, 403)

    def testWrongUserCannotEdit(self):
        other_user = self.createUser("bob")
        r = test_replays.CreateAsPublishedReplay("th10_normal", other_user)

        response = self._Post(r.shot.game.game_id, r.id, {})
        self.assertEqual(response.status_code, 403)

    def testDisplaysPage(self):
        r = test_replays.CreateAsPublishedReplay("th10_normal", self.user)

        response = self._Get(r.shot.game.game_id, r.id)
        self.assertEqual(response.status_code, 200)

    def testEditsReplay(self):
        r = test_replays.CreateAsPublishedReplay(
            "th10_normal", self.user, category=models.Category.STANDARD
        )

        response = self._Post(
            r.shot.game.game_id,
            r.id,
            {
                "name": "AAAAAAAA",
                "score": 294127890,
                "category": models.Category.TAS,
                "video_link": "",
                "is_clear": True,
                "is_good": True,
                "uses_bombs": True,
                "misses": "",
                "comment": "nooblord",
            },
        )

        self.assertEqual(response.status_code, 302)

        target = urls.resolve(response.url)
        updated_replay = models.Replay.objects.get(
            id=target.captured_kwargs["replay_id"]
        )

        self.assertEqual(updated_replay.category, models.Category.TAS)

    def testEditsReplay(self):
        r = test_replays.CreateAsPublishedReplay(
            "th10_normal", self.user, category=models.Category.STANDARD
        )

        response = self._Post(
            r.shot.game.game_id,
            r.id,
            {
                "name": "AAAAAAAA",
                "score": 294127890,
                "category": models.Category.TAS,
                "video_link": "https://not_a_valid_site.example",
                "is_clear": True,
                "is_good": True,
                "uses_bombs": True,
                "misses": "",
                "comment": "",
            },
        )

        self.assertIsInstance(response, template_response.TemplateResponse)
        self.assertEqual(response.status_code, 200)
        response_form = response.context_data["form"]
        self.assertIn("video_link", response_form.errors)

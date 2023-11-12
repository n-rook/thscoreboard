from django import test as django_test
from django import urls

from replays import game_ids
from replays.views import replay_list
from replays.testing import test_case


class GameScoreboardRedirectTestCase(test_case.ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.factory = django_test.RequestFactory()

    def _Get(self, game_id, difficulty, shot_id=None):
        kwargs = {"game_id": game_id, "difficulty": difficulty}
        if shot_id is not None:
            kwargs["shot_id"] = shot_id
        url = urls.reverse("Replays/GameScoreboardOldRedirect", kwargs=kwargs)

        request = self.factory.get(url)
        return replay_list.game_scoreboard_old_url(request, **kwargs)

    def testRedirectsWithShot(self):
        response = self._Get(game_ids.GameIDs.TH07, difficulty=1, shot_id="ReimuA")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            urls.reverse("Replays/GameScoreboard", args=[game_ids.GameIDs.TH07]),
        )

    def testRedirectsWithoutShot(self):
        response = self._Get(game_ids.GameIDs.TH07, difficulty=1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            urls.reverse("Replays/GameScoreboard", args=[game_ids.GameIDs.TH07]),
        )

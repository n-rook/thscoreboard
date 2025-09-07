from django import test as django_test
from django import urls
from replays import models

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


class GetFilterOptionsTestCase(test_case.ReplayTestCase):
    def assertHasFilterWithNValues(self, expected_name, expected_length, filters):
        for f in filters:
            if f.name == expected_name:
                break
        else:
            self.fail(f"No filter in {filters} with name {expected_name}")
        self.assertEqual(len(f.values), expected_length)

    def test_default(self):
        game = models.Game.objects.get(game_id=game_ids.GameIDs.TH06)
        filter_options = replay_list.get_filter_options(game)
        self.assertEqual(len(filter_options), 2)
        self.assertHasFilterWithNValues("Difficulty", 5, filter_options)
        self.assertHasFilterWithNValues("Shot", 4, filter_options)

    def test_th01(self):
        game = models.Game.objects.get(game_id=game_ids.GameIDs.TH01)
        filter_options = replay_list.get_filter_options(game)
        self.assertEqual(len(filter_options), 2)
        self.assertHasFilterWithNValues("Difficulty", 4, filter_options)
        self.assertHasFilterWithNValues("Route", 2, filter_options)

    def test_th08(self):
        game = models.Game.objects.get(game_id=game_ids.GameIDs.TH08)
        filter_options = replay_list.get_filter_options(game)
        self.assertEqual(len(filter_options), 3)
        self.assertHasFilterWithNValues("Difficulty", 5, filter_options)
        self.assertHasFilterWithNValues("Route", 2, filter_options)
        self.assertHasFilterWithNValues("Shot", 12, filter_options)

    def test_th13(self):
        game = models.Game.objects.get(game_id=game_ids.GameIDs.TH13)
        filter_options = replay_list.get_filter_options(game)
        self.assertEqual(len(filter_options), 2)
        self.assertHasFilterWithNValues("Difficulty", 5, filter_options)
        self.assertHasFilterWithNValues("Shot", 4, filter_options)

    def test_th16(self):
        game = models.Game.objects.get(game_id=game_ids.GameIDs.TH16)
        filter_options = replay_list.get_filter_options(game)
        self.assertEqual(len(filter_options), 3)
        self.assertHasFilterWithNValues("Difficulty", 5, filter_options)
        self.assertHasFilterWithNValues("Character", 4, filter_options)
        self.assertHasFilterWithNValues("Season", 4, filter_options)

    def test_th17(self):
        game = models.Game.objects.get(game_id=game_ids.GameIDs.TH17)
        filter_options = replay_list.get_filter_options(game)
        self.assertEqual(len(filter_options), 3)
        self.assertHasFilterWithNValues("Difficulty", 5, filter_options)
        self.assertHasFilterWithNValues("Character", 3, filter_options)
        self.assertHasFilterWithNValues("Goast", 3, filter_options)

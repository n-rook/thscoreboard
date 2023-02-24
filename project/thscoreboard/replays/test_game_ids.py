from django import test

from replays import game_ids
from replays import models
from replays.testing import test_case


class GameIDsTestCase(test.SimpleTestCase):
    
    def testGetLongName(self):
        eosd_name = game_ids.GetGameName(game_id=game_ids.GameIDs.TH06, short=False)
        self.assertIn('Embodiment of Scarlet Devil', eosd_name)

    def testGetShortName(self):
        # https://github.com/n-rook/thscoreboard/issues/58
        # gettext doesn't work right on the GitHub bot, so we intentionally
        # override it with a language for which we don't have translations.
        with test.override_settings(LANGUAGE_CODE='pt-br'):
            eosd_name = game_ids.GetGameName(game_id=game_ids.GameIDs.TH06, short=True)
        self.assertEqual('th06', eosd_name)

    def testGetShotName(self):
        shot_name = game_ids.GetShotName(game_id=game_ids.GameIDs.TH06, shot_id='ReimuA')
        self.assertEqual(shot_name, 'Reimu A')

    def testGetDifficultyName(self):
        difficulty_name = game_ids.GetDifficultyName(game_id=game_ids.GameIDs.TH06, difficulty=0)
        self.assertEqual(difficulty_name, 'Easy')

    def testGetRouteName(self):
        difficulty_name = game_ids.GetRouteName(game_id=game_ids.GameIDs.TH01, route_id='Jigoku')
        self.assertEqual(difficulty_name, 'Jigoku')


class GameIDsComprehensiveTestCase(test_case.ReplayTestCase):

    def AssertNoBug(self, thing_name):
        """Assert that some name does not include the word bug.

        Conventionally we call all of our buggy "nothing matches" names things
        like "Bug name", so this will fail if those exist.

        Args:
            thing_name: The name of the thing to check.
        """
        self.assertNotIn('bug', thing_name.lower())

    def testNoBugNamesForGames(self):
        games = models.Game.objects.all()
        for game in games:
            game_name = game_ids.GetGameName(game.game_id)
            self.AssertNoBug(game_name)

    def testNoBugShortNamesForGames(self):
        games = models.Game.objects.all()
        for game in games:
            game_name = game_ids.GetGameName(game.game_id, short=True)
            self.AssertNoBug(game_name)

    def testNoBugDifficultyNamesForGames(self):
        games = models.Game.objects.all()
        for game in games:
            for difficulty in range(game.num_difficulties):
                self.AssertNoBug(
                    game_ids.GetDifficultyName(game_id=game.game_id, difficulty=difficulty)
                )

    def testNoBugShotNamesForGames(self):
        games = models.Game.objects.all()
        for game in games:
            shots = models.Shot.objects.filter(game=game.game_id)
            for shot in shots:
                self.AssertNoBug(
                    game_ids.GetShotName(game_id=game.game_id, shot_id=shot.shot_id)
                )
    
    def testNoBugRouteNamesForGames(self):
        games = models.Game.objects.all()
        for game in games:
            routes = models.Route.objects.filter(game=game.game_id)
            for route in routes:
                self.AssertNoBug(
                    game_ids.GetRouteName(game_id=game.game_id, route_id=route.route_id)
                )


class ReplayIdTestCase(test.SimpleTestCase):
    
    def testMakeReplayId(self):
        self.assertEqual(game_ids.MakeReplayId(1679615), 'zzzz')
        self.assertEqual(game_ids.MakeReplayId(1679616), '10000')
        self.assertEqual(game_ids.MakeReplayId(3 * 36 + 1), '0031')
        self.assertEqual(game_ids.MakeReplayId(0), '0000')

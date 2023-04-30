from django import test

from replays import game_ids
from replays import models
from replays.testing import test_case
from replays.testing import test_utilities


class GameIDsTestCase(test.SimpleTestCase):
    def testGetGameName(self):
        with test_utilities.OverrideTranslations():
            short = game_ids.GetGameName(
                game_id=game_ids.GameIDs.TH06, name_length=game_ids.NameLength.SHORT
            )
            standard = game_ids.GetGameName(
                game_id=game_ids.GameIDs.TH06, name_length=game_ids.NameLength.STANDARD
            )
            full = game_ids.GetGameName(
                game_id=game_ids.GameIDs.TH06, name_length=game_ids.NameLength.FULL
            )

        self.assertEqual("th06", short)
        self.assertEqual("Embodiment of Scarlet Devil", standard)
        self.assertEqual("東方紅魔郷 - Embodiment of Scarlet Devil", full)

    def testGetShotName(self):
        shot_name = game_ids.GetShotName(
            game_id=game_ids.GameIDs.TH06, shot_id="ReimuA"
        )
        self.assertEqual(shot_name, "Reimu A")

    def testGetDifficultyName(self):
        difficulty_name = game_ids.GetDifficultyName(
            game_id=game_ids.GameIDs.TH06, difficulty=0
        )
        self.assertEqual(difficulty_name, "Easy")

    def testGetRouteName(self):
        difficulty_name = game_ids.GetRouteName(
            game_id=game_ids.GameIDs.TH01, route_id="Jigoku"
        )
        self.assertEqual(difficulty_name, "Jigoku")

    def testHasBombs(self):
        cases = [
            ["TH05", game_ids.GameIDs.TH05, None, True],
            ["TH06", game_ids.GameIDs.TH06, None, True],
            ["TH09", game_ids.GameIDs.TH09, None, False],
            ["TH13", game_ids.GameIDs.TH13, None, True],
            ["TH13_Full", game_ids.GameIDs.TH13, game_ids.ReplayTypes.FULL_GAME, True],
            [
                "TH13_SpellPractice",
                game_ids.GameIDs.TH13,
                game_ids.ReplayTypes.SPELL_PRACTICE,
                False,
            ],
        ]

        for name, game_id, replay_type, expected_outcome in cases:
            with self.subTest(name):
                self.assertIs(
                    bool(game_ids.HasBombs(game_id, replay_type=replay_type)),
                    expected_outcome,
                )

    def testHasLives(self):
        cases = [
            ["TH05", game_ids.GameIDs.TH05, None, True],
            ["TH06", game_ids.GameIDs.TH06, None, True],
            ["TH09", game_ids.GameIDs.TH09, None, True],
            ["TH13", game_ids.GameIDs.TH13, None, True],
            ["TH13_Full", game_ids.GameIDs.TH13, game_ids.ReplayTypes.FULL_GAME, True],
            [
                "TH13_SpellPractice",
                game_ids.GameIDs.TH13,
                game_ids.ReplayTypes.SPELL_PRACTICE,
                False,
            ],
        ]

        for name, game_id, replay_type, expected_outcome in cases:
            with self.subTest(name):
                self.assertIs(
                    bool(game_ids.HasLives(game_id, replay_type=replay_type)),
                    expected_outcome,
                )


class GameIDsComprehensiveTestCase(test_case.ReplayTestCase):
    def AssertNoBug(self, thing_name):
        """Assert that some name does not include the word bug.

        Conventionally we call all of our buggy "nothing matches" names things
        like "Bug name", so this will fail if those exist.

        Args:
            thing_name: The name of the thing to check.
        """
        self.assertNotIn("bug", thing_name.lower())

    def testNoBugNamesForGames(self):
        games = models.Game.objects.all()
        for game in games:
            for name_length in game_ids.NameLength:
                game_name = game_ids.GetGameName(game.game_id, name_length=name_length)
                self.AssertNoBug(game_name)

    def testGameNamesAreLongerWithLongerSpecifiers(self):
        games = models.Game.objects.all()
        for game in games:
            with self.subTest(game.game_id):
                short = game_ids.GetGameName(
                    game.game_id, name_length=game_ids.NameLength.SHORT
                )
                standard = game_ids.GetGameName(
                    game.game_id, name_length=game_ids.NameLength.STANDARD
                )
                full = game_ids.GetGameName(
                    game.game_id, name_length=game_ids.NameLength.FULL
                )

                self.assertLess(len(short), len(standard))
                self.assertLess(len(standard), len(full))

    def testNoBugDifficultyNamesForGames(self):
        games = models.Game.objects.all()
        for game in games:
            for difficulty in range(game.num_difficulties):
                self.AssertNoBug(
                    game_ids.GetDifficultyName(
                        game_id=game.game_id, difficulty=difficulty
                    )
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
    def testMakeBase36ReplayId(self):
        self.assertEqual(game_ids.MakeBase36ReplayId(1679615), "zzzz")
        self.assertEqual(game_ids.MakeBase36ReplayId(1679616), "10000")
        self.assertEqual(game_ids.MakeBase36ReplayId(3 * 36 + 1), "0031")
        self.assertEqual(game_ids.MakeBase36ReplayId(0), "0000")

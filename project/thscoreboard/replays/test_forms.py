import unittest

from replays.testing.test_case import ReplayTestCase
from replays import forms
from replays import game_ids
from replays import models


class PublishReplayFormTest(unittest.TestCase):
    def testUsesBombs_Included(self):
        f = forms.PublishReplayForm(game_ids.GameIDs.TH06, models.ReplayType.FULL_GAME)
        self.assertIn("uses_bombs", f.fields)

    def testUsesBombs_NotIncludedForTH09(self):
        f = forms.PublishReplayForm(game_ids.GameIDs.TH09, models.ReplayType.FULL_GAME)
        self.assertNotIn("uses_bombs", f.fields)

    def testUsesBombs_NotIncludedForSpellPractice(self):
        f = forms.PublishReplayForm(
            game_ids.GameIDs.TH13, models.ReplayType.SPELL_PRACTICE
        )
        self.assertNotIn("uses_bombs", f.fields)

    def testMisses_Included(self):
        f = forms.PublishReplayForm(game_ids.GameIDs.TH06, models.ReplayType.FULL_GAME)
        self.assertIn("misses", f.fields)

    def testMisses_NotIncludedForSpellPractice(self):
        f = forms.PublishReplayForm(
            game_ids.GameIDs.TH13, models.ReplayType.SPELL_PRACTICE
        )
        self.assertNotIn("misses", f.fields)


class PublishReplayWithoutFileFormTest(ReplayTestCase):
    def testPvpReplayType_Included(self):
        th03 = models.Game.objects.get(game_id="th03")
        f = forms.PublishReplayWithoutFileForm(game=th03)
        replay_type_choices = [entry[1] for entry in f.fields["replay_type"].choices]
        self.assertIn("PVP", replay_type_choices)

    def testPvpReplayType_NotIncluded(self):
        game_ids_without_pvp = [
            game_ids.GameIDs.TH01,
            game_ids.GameIDs.TH02,
            game_ids.GameIDs.TH04,
            game_ids.GameIDs.TH05,
        ]
        for game_id in game_ids_without_pvp:
            with self.subTest():
                game = models.Game.objects.get(game_id=game_id)
                f = forms.PublishReplayWithoutFileForm(game=game)
                replay_type_choices = [
                    entry[1] for entry in f.fields["replay_type"].choices
                ]
                self.assertNotIn("PVP", replay_type_choices)

import unittest

from replays import forms
from replays import game_ids
from replays import models


class PublishReplayFormTest(unittest.TestCase):
    def testUsesBombs_Included(self):
        f = forms.PublishReplayForm(game_ids.GameIDs.TH06, models.ReplayType.REGULAR)
        self.assertIn("uses_bombs", f.fields)

    def testUsesBombs_NotIncludedForTH09(self):
        f = forms.PublishReplayForm(game_ids.GameIDs.TH09, models.ReplayType.REGULAR)
        self.assertNotIn("uses_bombs", f.fields)

    def testUsesBombs_NotIncludedForSpellPractice(self):
        f = forms.PublishReplayForm(
            game_ids.GameIDs.TH13, models.ReplayType.SPELL_PRACTICE
        )
        self.assertNotIn("uses_bombs", f.fields)

    def testMisses_Included(self):
        f = forms.PublishReplayForm(game_ids.GameIDs.TH06, models.ReplayType.REGULAR)
        self.assertIn("misses", f.fields)

    def testMisses_NotIncludedForSpellPractice(self):
        f = forms.PublishReplayForm(
            game_ids.GameIDs.TH13, models.ReplayType.SPELL_PRACTICE
        )
        self.assertNotIn("misses", f.fields)

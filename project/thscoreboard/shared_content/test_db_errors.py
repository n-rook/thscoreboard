from django.db import utils

from shared_content import db_errors

from replays import models
from replays.testing import test_case
from replays.testing import test_replays


class DbErrorsTest(test_case.ReplayTestCase):
    def testRecognizesUniqueViolation(self):
        game = models.Game(game_id="th999", has_replays=True, num_difficulties=5)
        game.save()

        shot = models.Shot(game=game, shot_id="foo")
        shot.save()

        dupe_shot = models.Shot(game=game, shot_id="foo")

        try:
            dupe_shot.save()
        except utils.IntegrityError as e:
            self.assertTrue(db_errors.IsUniqueError(e))
            self.assertEqual(
                db_errors.GetUniqueConstraintCause(e), "unique_shot_per_game"
            )
        else:
            self.fail("Unexpected failure to raise an error")

    def testDoesNotThinkOtherViolationIsUnique(self):
        user = self.createUser("user")
        replay = test_replays.CreateAsPublishedReplay("th6_extra", user=user)
        replay.difficulty = -5

        try:
            replay.save()
        except utils.IntegrityError as e:
            self.assertFalse(db_errors.IsUniqueError(e))
        else:
            self.fail("Unexpected failure to raise an error")

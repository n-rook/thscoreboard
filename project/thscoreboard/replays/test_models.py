
import datetime

from replays import game_ids
from replays import models
from replays import create_replay
from replays import replay_parsing
from replays.testing import test_case
from replays.testing import test_replays

import django.db.utils

REPLAY_1 = test_replays.GetRaw('th6_extra')
REPLAY_2 = test_replays.GetRaw('th10_normal')


class TemporaryReplayFileTest(test_case.ReplayTestCase):

    def setUp(self):
        super().setUp()
        self.user = self.createUser('somebody')

    def testCleanUpDoesNothingWithNoReplays(self):

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        models.TemporaryReplayFile.CleanUp(now)

    def testCleanUpDeletesOldReplaysButNotNewOnes(self):

        now = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)

        delete_me = models.TemporaryReplayFile(
            user=self.user,
            replay=REPLAY_1,
            created=now - datetime.timedelta(days=32)
        )
        delete_me.save()

        dont_delete_me = models.TemporaryReplayFile(
            user=self.user,
            replay=REPLAY_2,
            created=now - datetime.timedelta(days=28)
        )
        dont_delete_me.save()

        models.TemporaryReplayFile.CleanUp(now)

        with self.assertRaises(models.TemporaryReplayFile.DoesNotExist):
            models.TemporaryReplayFile.objects.get(id=delete_me.id)
        
        models.TemporaryReplayFile.objects.get(id=dont_delete_me.id)
        # No exception; it does exist.


class TestConstraints(test_case.ReplayTestCase):

    def setUp(self):
        super().setUp()
        self.user = self.createUser('somebody')

    def testReplayTypeConstraint(self):

        shot = models.Shot.objects.get(game_id=game_ids.GameIDs.TH05, shot_id='Mima')

        with self.assertRaises(django.db.utils.IntegrityError):
            create_replay.PublishReplayWithoutFile(
                user=self.user,
                difficulty=1,
                shot=shot,
                score=10000,
                category=models.Category.REGULAR,
                comment='Hello',
                is_clear=True,
                video_link='https://www.youtube.com/example',
                route=None,
                replay_type=game_ids.ReplayTypes.SPELL_PRACTICE,
            )

    def testReplayTypeConstraint2(self):
        replay_file_contents = test_replays.GetRaw('th8_spell_practice')

        temp_replay = models.TemporaryReplayFile(
            user=self.user,
            replay=replay_file_contents
        )
        temp_replay.save()
        replay_info = replay_parsing.Parse(replay_file_contents)
        shot = models.Shot.objects.get(game=replay_info.game, shot_id=replay_info.shot)
        
        replay_info.replay_type = game_ids.ReplayTypes.REGULAR

        with self.assertRaises(django.db.utils.IntegrityError):
            create_replay.PublishNewReplay(
                user=self.user,
                difficulty=replay_info.difficulty,
                shot=shot,
                score=replay_info.score,
                category=models.Category.REGULAR,
                comment='',
                video_link='',
                is_good=True,
                is_clear=True,
                temp_replay_instance=temp_replay,
                replay_info=replay_info,
            )

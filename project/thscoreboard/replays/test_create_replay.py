
import datetime

from replays import game_ids
from replays import models
from replays import create_replay
from replays import replay_parsing
from replays.testing import test_case
from replays.testing import test_replays


class GameIDsComprehensiveTestCase(test_case.ReplayTestCase):

    def setUp(self):
        super().setUp()
        self.user = self.createUser('some-user')

    def testPublishWithoutReplayFile(self):
        shot = models.Shot.objects.get(game_id=game_ids.GameIDs.TH05, shot_id='Mima')

        new_replay = create_replay.PublishReplayWithoutFile(
            user=self.user,
            difficulty=1,
            shot=shot,
            score=10000,
            category=models.Category.REGULAR,
            comment='Hello',
            is_clear=True,
            video_link='https://www.youtube.com/example',
            route=None,
            replay_type=game_ids.ReplayTypes.REGULAR,
        )

        self.assertEqual(new_replay.user, self.user)
        self.assertEqual(new_replay.GetDifficultyName(), 'Normal')
        self.assertEqual(new_replay.shot, shot)
        self.assertEqual(new_replay.score, 10000)
        self.assertIsNone(new_replay.rep_score)
        self.assertTrue(new_replay.is_clear)
        self.assertEqual(new_replay.video_link, 'https://www.youtube.com/example')
        self.assertEqual(new_replay.comment, 'Hello')

        self.assertEqual(
            new_replay,
            models.Replay.objects.get(id=new_replay.id)
        )

    def testPublishReplay(self):
        replay_file_contents = test_replays.GetRaw('th10_normal')

        temp_replay = models.TemporaryReplayFile(
            user=self.user,
            replay=replay_file_contents
        )
        temp_replay.save()

        replay_info = replay_parsing.Parse(replay_file_contents)

        shot = models.Shot.objects.get(game='th10', shot_id='ReimuB')

        new_replay = create_replay.PublishNewReplay(
            user=self.user,
            difficulty=3,
            shot=shot,
            score=294127890,
            category=models.Category.REGULAR,
            comment='Hello',
            video_link='',
            is_good=True,
            is_clear=False,
            temp_replay_instance=temp_replay,
            replay_info=replay_info,
        )

        self.assertEqual(new_replay.user, self.user)
        self.assertEqual(new_replay.GetDifficultyName(), 'Lunatic')
        self.assertEqual(new_replay.shot, shot)
        self.assertEqual(new_replay.score, 294127890)
        self.assertEqual(new_replay.rep_score, 294127890)
        self.assertFalse(new_replay.is_clear)
        self.assertEqual(new_replay.category, models.Category.REGULAR)
        self.assertEqual(new_replay.comment, 'Hello')
        self.assertEqual(new_replay.replay_type, 1)
        self.assertEqual(new_replay.timestamp, datetime.datetime(2018, 2, 19, 4, 44, 21, tzinfo=datetime.timezone.utc))

        with self.assertRaises(models.TemporaryReplayFile.DoesNotExist):
            models.TemporaryReplayFile.objects.get(id=temp_replay.id)

    def testPublishReplaySavesStages_TH10(self):
        replay_file_contents = test_replays.GetRaw('th10_normal')

        temp_replay = models.TemporaryReplayFile(
            user=self.user,
            replay=replay_file_contents
        )
        temp_replay.save()

        replay_info = replay_parsing.Parse(replay_file_contents)

        shot = models.Shot.objects.get(game='th10', shot_id='ReimuB')

        new_replay = create_replay.PublishNewReplay(
            user=self.user,
            difficulty=3,
            shot=shot,
            score=294127890,
            category=models.Category.REGULAR,
            comment='',
            video_link='',
            is_good=True,
            is_clear=True,
            temp_replay_instance=temp_replay,
            replay_info=replay_info,
        )

        stages = list(models.ReplayStage.objects.filter(replay=new_replay))
        self.assertEqual(len(stages), 6)

        self.assertEqual(stages[0].score, 12996310)

    def testPublishReplaySpellPractice(self):
        replay_file_contents = test_replays.GetRaw('th8_spell_practice')

        temp_replay = models.TemporaryReplayFile(
            user=self.user,
            replay=replay_file_contents
        )
        temp_replay.save()
        replay_info = replay_parsing.Parse(replay_file_contents)
        shot = models.Shot.objects.get(game=replay_info.game, shot_id=replay_info.shot)
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

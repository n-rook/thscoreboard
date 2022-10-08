from os import path

from django import test

from replays import game_ids
from replays import models
from replays import create_replay
from replays import replay_parsing
from replays.testing import test_case

def ReadTestFile(filename):
    with open(path.join('replays/replays_for_tests', filename), 'rb') as f:
        return f.read()


class GameIDsComprehensiveTestCase(test_case.ReplayTestCase):

    def setUp(self):
        super().setUp()
        self.user = self.createUser('some-user')

    def testPublishWithoutReplayFile(self):
        shot = models.Shot.objects.get(shot_id='Mima')

        new_replay = create_replay.PublishReplayWithoutFile(
            user=self.user,
            difficulty=1,
            shot=shot,
            points=10000,
            category=models.Category.REGULAR,
            comment='Hello',
            video_link='https://www.youtube.com/example',
            route=None,
        )

        self.assertEqual(new_replay.user, self.user)
        self.assertEqual(new_replay.GetDifficultyName(), 'Normal')
        self.assertEqual(new_replay.shot, shot)
        self.assertEqual(new_replay.points, 10000)
        self.assertIsNone(new_replay.rep_points)
        self.assertEqual(new_replay.video_link, 'https://www.youtube.com/example')
        self.assertEqual(new_replay.comment, 'Hello')

        self.assertEqual(
            new_replay,
            models.Replay.objects.get(id=new_replay.id)
        )
    
    def testPublishReplay(self):
        # with open(path.join('replays/replays_for_tests', 'th10_normal.rpy'), 'rb') as f:
            # replay_file_contents = f.read()
        replay_file_contents = ReadTestFile('th10_normal.rpy')
        
        temp_replay = models.TemporaryReplayFile(
            user=self.user,
            replay=replay_file_contents
        )
        temp_replay.save()

        replay_info = replay_parsing.Parse(replay_file_contents)

        shot = models.Shot.objects.get(game='th10', shot_id='ReimuB')

        new_replay = create_replay.PublishNewReplay(
            user=self.user,
            difficulty=1,
            shot=shot,
            points=12345,
            category=models.Category.REGULAR,
            comment='Hello',
            video_link='',
            is_good=True,
            temp_replay_instance=temp_replay,
            replay_info=replay_info,
        )

        self.assertEqual(new_replay.user, self.user)
        self.assertEqual(new_replay.GetDifficultyName(), 'Normal')
        self.assertEqual(new_replay.shot, shot)
        self.assertEqual(new_replay.points, 12345)
        self.assertEqual(new_replay.rep_points, 12345)
        self.assertEqual(new_replay.category, models.Category.REGULAR)
        self.assertEqual(new_replay.comment, 'Hello')

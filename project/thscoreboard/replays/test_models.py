from replays import game_ids
from replays import models
from replays import create_replay
from replays import replay_parsing
from replays.testing import test_case
from replays.testing import test_replays

import django.db.utils

REPLAY_1 = test_replays.GetRaw('th6_extra')
REPLAY_2 = test_replays.GetRaw('th10_normal')


class ReplayTest(test_case.ReplayTestCase):

    def setUp(self):
        super().setUp()
        self.author = self.createUser('author')
        self.viewer = self.createUser('viewer')

    def testVisible(self):
        should_be_visible = test_replays.CreateAsPublishedReplay(
            filename='th6_extra',
            user=self.author,
            category=models.Category.REGULAR
        )

        self.assertTrue(should_be_visible.IsVisible(viewer=None))
        self.assertTrue(models.Replay.objects.visible_to(viewer=None).filter(id=should_be_visible.id).exists())

        self.assertTrue(should_be_visible.IsVisible(viewer=self.viewer))
        self.assertTrue(models.Replay.objects.visible_to(viewer=self.viewer).filter(id=should_be_visible.id).exists())

    def testVisible_AuthorDeletedAccount(self):
        should_be_visible = test_replays.CreateAsPublishedReplay(
            filename='th6_extra',
            user=self.author,
            category=models.Category.REGULAR
        )
        self.author.MarkForDeletion()

        self.assertFalse(should_be_visible.IsVisible(viewer=None))
        self.assertFalse(models.Replay.objects.visible_to(viewer=None).filter(id=should_be_visible.id).exists())

        self.assertFalse(should_be_visible.IsVisible(viewer=self.viewer))
        self.assertFalse(models.Replay.objects.visible_to(viewer=self.viewer).filter(id=should_be_visible.id).exists())

    def testVisible_PENDING(self):
        should_be_visible = test_replays.CreateAsPublishedReplay(
            filename='th6_extra',
            user=self.author,
            category=models.Category.PENDING
        )

        self.assertFalse(should_be_visible.IsVisible(viewer=None))
        self.assertFalse(models.Replay.objects.visible_to(viewer=None).filter(id=should_be_visible.id).exists())

        self.assertFalse(should_be_visible.IsVisible(viewer=self.viewer))
        self.assertFalse(models.Replay.objects.visible_to(viewer=self.viewer).filter(id=should_be_visible.id).exists())

        self.assertTrue(should_be_visible.IsVisible(viewer=self.author))
        self.assertTrue(models.Replay.objects.visible_to(viewer=self.author).filter(id=should_be_visible.id).exists())


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

        replay_info = replay_parsing.Parse(replay_file_contents)
        replay_info.replay_type = game_ids.ReplayTypes.REGULAR

        with self.assertRaises(django.db.utils.IntegrityError):
            create_replay.PublishNewReplay(
                user=self.user,
                category=models.Category.REGULAR,
                comment='',
                video_link='',
                is_good=True,
                is_clear=True,
                file=replay_file_contents,
                replay_info=replay_info,
            )

    def testReplayPendingConstraint1(self):
        replay_file_contents = test_replays.GetRaw('th7_extra')
        replay_info = replay_parsing.Parse(replay_file_contents)

        with self.assertRaises(django.db.utils.IntegrityError):
            create_replay.PublishNewReplay(
                user=self.user,
                category=models.Category.REGULAR,
                comment='',
                video_link='',
                is_good=True,
                is_clear=None,
                file=replay_file_contents,
                replay_info=replay_info
            )

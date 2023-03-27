import datetime

from replays import game_ids
from replays import models
from replays import constant_helpers
from replays import create_replay
from replays import replay_parsing
from replays.testing import test_case
from replays.testing import test_replays

import django.db.utils

REPLAY_1 = test_replays.GetRaw("th6_extra")
REPLAY_2 = test_replays.GetRaw("th10_normal")


class ReplayTest(test_case.ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.author = self.createUser("author")
        self.viewer = self.createUser("viewer")

    def testVisible(self):
        should_be_visible = test_replays.CreateAsPublishedReplay(
            filename="th6_extra", user=self.author, category=models.Category.REGULAR
        )

        self.assertTrue(should_be_visible.IsVisible())
        self.assertTrue(
            models.Replay.objects.filter_visible()
            .filter(id=should_be_visible.id)
            .exists()
        )

    def testVisible_AuthorDeletedAccount(self):
        should_be_visible = test_replays.CreateAsPublishedReplay(
            filename="th6_extra", user=self.author, category=models.Category.REGULAR
        )
        self.author.MarkForDeletion()

        self.assertFalse(should_be_visible.IsVisible())
        self.assertFalse(
            models.Replay.objects.filter_visible()
            .filter(id=should_be_visible.id)
            .exists()
        )

        self.assertFalse(should_be_visible.IsVisible())
        self.assertFalse(
            models.Replay.objects.filter_visible()
            .filter(id=should_be_visible.id)
            .exists()
        )

    def testSetFromConstantHelpers_WithRoute(self):
        to_be_modified = test_replays.CreateAsPublishedReplay(
            "th7_lunatic", self.author
        )

        th08 = models.Game.objects.get(game_id="th08")
        new_constants = constant_helpers.ReplayConstantModels(
            game=th08,
            shot=models.Shot.objects.get(game=th08, shot_id="Marisa & Alice"),
            route=models.Route.objects.get(route_id="Final A"),
        )

        to_be_modified.SetForeignKeysFromConstantModels(new_constants)
        self.assertEqual(to_be_modified.shot.game.game_id, "th08")
        self.assertEqual(to_be_modified.shot.shot_id, "Marisa & Alice")
        self.assertEqual(to_be_modified.route.route_id, "Final A")

    def testSetFromConstantHelpers_NoRoute(self):
        to_be_modified = test_replays.CreateAsPublishedReplay("th8_normal", self.author)

        th08 = models.Game.objects.get(game_id="th08")
        new_constants = constant_helpers.ReplayConstantModels(
            game=th08,
            shot=models.Shot.objects.get(game=th08, shot_id="Marisa & Alice"),
            route=None,
        )

        to_be_modified.SetForeignKeysFromConstantModels(new_constants)
        self.assertEqual(to_be_modified.shot.game.game_id, "th08")
        self.assertEqual(to_be_modified.shot.shot_id, "Marisa & Alice")
        self.assertIsNone(to_be_modified.route)


class TemporaryReplayFileTest(test_case.ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.createUser("somebody")

    def testCleanUpDoesNothingWithNoReplays(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        models.TemporaryReplayFile.CleanUp(now)

    def testCleanUpDeletesOldReplaysButNotNewOnes(self):
        now = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)

        delete_me = models.TemporaryReplayFile(
            user=self.user, replay=REPLAY_1, created=now - datetime.timedelta(days=32)
        )
        delete_me.save()

        dont_delete_me = models.TemporaryReplayFile(
            user=self.user, replay=REPLAY_2, created=now - datetime.timedelta(days=28)
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
        self.user = self.createUser("somebody")

    def testReplayTypeConstraint(self):
        shot = models.Shot.objects.get(game_id=game_ids.GameIDs.TH05, shot_id="Mima")

        with self.assertRaises(django.db.utils.IntegrityError):
            create_replay.PublishReplayWithoutFile(
                user=self.user,
                difficulty=1,
                shot=shot,
                score=10000,
                category=models.Category.REGULAR,
                comment="Hello",
                is_clear=True,
                video_link="https://www.youtube.com/example",
                route=None,
                replay_type=game_ids.ReplayTypes.SPELL_PRACTICE,
                no_bomb=False,
                miss_count=None,
            )

    def testReplayTypeConstraint2(self):
        replay_file_contents = test_replays.GetRaw("th8_spell_practice")

        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()
        replay_info = replay_parsing.Parse(replay_file_contents)
        replay_info.replay_type = game_ids.ReplayTypes.REGULAR

        with self.assertRaises(django.db.utils.IntegrityError):
            create_replay.PublishNewReplay(
                user=self.user,
                difficulty=replay_info.difficulty,
                score=replay_info.score,
                category=models.Category.REGULAR,
                comment="",
                video_link="",
                is_good=True,
                is_clear=True,
                temp_replay_instance=temp_replay,
                replay_info=replay_info,
                no_bomb=False,
                miss_count=None,
            )

import datetime
import logging
from unittest.mock import patch

from replays import game_ids
from replays import limits
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
            filename="th6_extra", user=self.author, category=models.Category.STANDARD
        )

        self.assertTrue(should_be_visible.IsVisible())
        self.assertTrue(
            models.Replay.objects.filter_visible()
            .filter(id=should_be_visible.id)
            .exists()
        )

    def testVisible_AuthorDeletedAccount(self):
        should_be_visible = test_replays.CreateAsPublishedReplay(
            filename="th6_extra", user=self.author, category=models.Category.STANDARD
        )
        self.author.MarkForDeletion()

        self.assertFalse(should_be_visible.IsVisible())
        self.assertFalse(
            models.Replay.objects.filter_visible()
            .filter(id=should_be_visible.id)
            .exists()
        )

    def testVisible_Imported_username(self):
        should_be_visible = test_replays.CreateAsPublishedReplay(
            filename="th6_extra",
            user=None,
            category=models.Category.STANDARD,
            imported_username="あ",
        )

        self.assertTrue(should_be_visible.IsVisible())
        self.assertTrue(
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

    def testGetShortenedComment_ShortComment(self) -> None:
        short_comment = "a" * limits.MAX_SHORTENED_COMMENT_LENGTH
        replay = test_replays.CreateAsPublishedReplay(
            filename="th6_extra", user=self.author, comment=short_comment
        )
        expected_shortened_comment = short_comment
        self.assertEqual(replay.GetShortenedComment(), expected_shortened_comment)

    def testGetShortenedComment_LongComment(self) -> None:
        long_comment = "a" * (limits.MAX_SHORTENED_COMMENT_LENGTH + 1)
        replay = test_replays.CreateAsPublishedReplay(
            filename="th6_extra", user=self.author, comment=long_comment
        )
        expected_shortened_comment = "a" * limits.MAX_SHORTENED_COMMENT_LENGTH + "..."
        self.assertEqual(replay.GetShortenedComment(), expected_shortened_comment)

    def testRanks(self):
        with patch("replays.constant_helpers.CalculateReplayFileHash") as mocked_hash:
            mocked_hash.return_value = bytes(0)
            test_replays.CreateAsPublishedReplay(
                filename="th6_extra",
                user=self.author,
                score=1_000_000_000,
            )
            mocked_hash.return_value = bytes(1)
            test_replays.CreateAsPublishedReplay(
                filename="th6_extra",
                user=self.author,
                score=900_000_000,
            )
            mocked_hash.return_value = bytes(2)
            test_replays.CreateAsPublishedReplay(
                filename="th7_extra",
                user=self.author,
                score=800_000_000,
            )

        replays = models.Replay.objects.order_by("-score").annotate_with_rank().all()

        self.assertEquals(replays[0].rank, 1)
        self.assertEquals(replays[1].rank, 2)
        self.assertEquals(replays[2].rank, 1)

    def testRanksTasReplay(self):
        test_replays.CreateAsPublishedReplay(
            filename="th6_extra",
            user=self.author,
            score=1_000_000_000,
            category=models.Category.TAS,
        )

        replay = models.Replay.objects.order_by("-score").annotate_with_rank().first()

        self.assertEquals(replay.rank, -1)

    def testRanksBreakTiesUsingUploadDate(self):
        with patch("replays.constant_helpers.CalculateReplayFileHash") as mocked_hash:
            mocked_hash.return_value = bytes(0)
            test_replays.CreateAsPublishedReplay(
                filename="th17_lunatic",
                user=self.author,
                score=9_999_999_990,
                created_timestamp=datetime.datetime(
                    2001, 1, 1, tzinfo=datetime.timezone.utc
                ),
            )
            mocked_hash.return_value = bytes(1)
            test_replays.CreateAsPublishedReplay(
                filename="th17_lunatic",
                user=self.author,
                score=9_999_999_990,
                created_timestamp=datetime.datetime(
                    2003, 3, 3, tzinfo=datetime.timezone.utc
                ),
            )
            mocked_hash.return_value = bytes(2)
            test_replays.CreateAsPublishedReplay(
                filename="th17_lunatic",
                user=self.author,
                score=9_999_999_990,
                created_timestamp=datetime.datetime(
                    2002, 2, 2, tzinfo=datetime.timezone.utc
                ),
            )

        replays = models.Replay.objects.order_by("created").annotate_with_rank().all()

        self.assertEquals(replays[0].rank, 1)
        self.assertEquals(replays[1].rank, 2)
        self.assertEquals(replays[2].rank, 3)

    def testStagePracticeReplaysAreUnranked(self) -> None:
        test_replays.CreateAsPublishedReplay(
            filename="th6_extra",
            user=self.author,
            replay_type=models.ReplayType.STAGE_PRACTICE,
        )

        replay = models.Replay.objects.annotate_with_rank().first()
        self.assertEquals(replay.rank, -1)

    def testGetFormattedTimestampDate_NoDate(self):
        th05_mima = models.Shot.objects.get(
            game_id=game_ids.GameIDs.TH05, shot_id="Mima"
        )

        r = create_replay.PublishReplayWithoutFile(
            user=self.author,
            difficulty=1,
            shot=th05_mima,
            score=10000,
            category=models.Category.STANDARD,
            comment="Hello",
            is_clear=True,
            video_link="https://www.youtube.com/example",
            route=None,
            replay_type=game_ids.ReplayTypes.FULL_GAME,
            no_bomb=False,
            miss_count=None,
        )

        self.assertIsNone(r.GetFormattedTimestampDate())

    def testGetFormattedTimestampDate_TH07(self):
        r = test_replays.CreateAsPublishedReplay(
            filename="th7_lunatic",
            user=self.author,
        )
        self.assertEqual(r.GetFormattedTimestampDate(), "22 October")

    def testGetFormattedTimestampDate_Regular(self):
        r = test_replays.CreateAsPublishedReplay(
            filename="th8_normal",
            user=self.author,
        )
        self.assertEqual(r.GetFormattedTimestampDate(), "25 May 2018")


class TemporaryReplayFileTest(test_case.ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.createUser("somebody")

    def testCleanUpDoesNothingWithNoReplays(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        with self.assertLogs(logging.getLogger(), level="INFO"):
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

        with self.assertLogs(logging.getLogger(), level="INFO"):
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
                category=models.Category.STANDARD,
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
        replay_info.replay_type = game_ids.ReplayTypes.FULL_GAME

        with self.assertRaises(django.db.utils.IntegrityError):
            create_replay.PublishNewReplay(
                user=self.user,
                difficulty=replay_info.difficulty,
                score=replay_info.score,
                category=models.Category.STANDARD,
                comment="",
                video_link="",
                is_good=True,
                is_clear=True,
                temp_replay_instance=temp_replay,
                replay_info=replay_info,
                no_bomb=False,
                miss_count=None,
            )

    def testUserOrImportedUsernameIsNonNullConstraint(self):
        replay_file_contents = test_replays.GetRaw("th8_spell_practice")

        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()
        replay_info = replay_parsing.Parse(replay_file_contents)

        with self.assertRaises(django.db.utils.IntegrityError):
            create_replay.PublishNewReplay(
                user=None,
                difficulty=replay_info.difficulty,
                score=replay_info.score,
                category=models.Category.STANDARD,
                comment="",
                video_link="",
                is_good=True,
                is_clear=True,
                temp_replay_instance=temp_replay,
                replay_info=replay_info,
                no_bomb=False,
                miss_count=None,
            )

import datetime

from replays import game_ids
from replays import models
from replays import create_replay
from replays import replay_parsing
from replays import constant_helpers
from replays.testing import test_case
from replays.testing import test_replays
from django import urls
from django.db import utils


class GameIDsComprehensiveTestCase(test_case.ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.createUser("some-user")

    def testPublishWithoutReplayFile(self):
        shot = models.Shot.objects.get(game_id=game_ids.GameIDs.TH05, shot_id="Mima")

        new_replay = create_replay.PublishReplayWithoutFile(
            user=self.user,
            difficulty=1,
            shot=shot,
            score=10000,
            category=models.Category.STANDARD,
            comment="Hello",
            is_clear=True,
            video_link="https://www.youtube.com/example",
            route=None,
            replay_type=game_ids.ReplayTypes.FULL_GAME,
            no_bomb=False,
            miss_count=3,
        )

        self.assertEqual(new_replay.user, self.user)
        self.assertEqual(new_replay.GetDifficultyName(), "Normal")
        self.assertEqual(new_replay.shot, shot)
        self.assertEqual(new_replay.score, 10000)
        self.assertIsNone(new_replay.rep_score)
        self.assertTrue(new_replay.is_clear)
        self.assertEqual(new_replay.video_link, "https://www.youtube.com/example")
        self.assertEqual(new_replay.comment, "Hello")
        self.assertFalse(new_replay.no_bomb)
        self.assertEqual(new_replay.miss_count, 3)

        self.assertEqual(new_replay, models.Replay.objects.get(id=new_replay.id))

    def testPublishReplay(self):
        replay_file_contents = test_replays.GetRaw("th10_normal")

        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()

        replay_info = replay_parsing.Parse(replay_file_contents)

        new_replay = create_replay.PublishNewReplay(
            user=self.user,
            difficulty=3,
            score=294127890,
            category=models.Category.STANDARD,
            comment="Hello",
            video_link="",
            is_good=True,
            is_clear=False,
            temp_replay_instance=temp_replay,
            replay_info=replay_info,
            no_bomb=False,
            miss_count=3,
        )

        shot = models.Shot.objects.get(game="th10", shot_id="ReimuB")

        self.assertEqual(new_replay.user, self.user)
        self.assertEqual(new_replay.GetDifficultyName(), "Lunatic")
        self.assertEqual(new_replay.shot, shot)
        self.assertEqual(new_replay.score, 294127890)
        self.assertEqual(new_replay.rep_score, 294127890)
        self.assertFalse(new_replay.is_clear)
        self.assertEqual(new_replay.category, models.Category.STANDARD)
        self.assertEqual(new_replay.comment, "Hello")
        self.assertEqual(new_replay.replay_type, 1)
        self.assertFalse(new_replay.no_bomb)
        self.assertEqual(new_replay.miss_count, 3)
        self.assertEqual(
            new_replay.timestamp,
            datetime.datetime(2018, 2, 19, 9, 44, 21, tzinfo=datetime.timezone.utc),
        )

        with self.assertRaises(models.TemporaryReplayFile.DoesNotExist):
            models.TemporaryReplayFile.objects.get(id=temp_replay.id)

    def testPublishReplaySavesRoutes_TH08(self):
        replay_file_contents = test_replays.GetRaw("th8_normal")

        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()

        replay_info = replay_parsing.Parse(replay_file_contents)

        new_replay = create_replay.PublishNewReplay(
            user=self.user,
            difficulty=replay_info.difficulty,
            score=replay_info.score,
            category=models.Category.STANDARD,
            comment="Hello",
            video_link="",
            is_good=True,
            is_clear=True,
            no_bomb=False,
            miss_count=None,
            temp_replay_instance=temp_replay,
            replay_info=replay_info,
        )

        self.assertIsNotNone(new_replay.route)
        self.assertEqual(new_replay.route.route_id, "Final B")

    def testPublishReplaySavesSceneGameLevelInteger_TH095(self):
        replay_file_contents = test_replays.GetRaw("th95_3-1")

        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()

        replay_info = replay_parsing.Parse(replay_file_contents)

        new_replay = create_replay.PublishNewReplay(
            user=self.user,
            difficulty=replay_info.difficulty,
            score=replay_info.score,
            category=models.Category.STANDARD,
            comment="Hello",
            video_link="",
            is_good=True,
            is_clear=True,
            no_bomb=False,
            miss_count=None,
            temp_replay_instance=temp_replay,
            replay_info=replay_info,
        )
        self.assertEqual(new_replay.scene_game_level, 3)
        self.assertEqual(new_replay.scene_game_scene, 1)

    def testPublishReplaySavesSceneGameLevelExtra_TH095(self):
        replay_file_contents = test_replays.GetRaw("th95_Ex-2")

        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()

        replay_info = replay_parsing.Parse(replay_file_contents)

        new_replay = create_replay.PublishNewReplay(
            user=self.user,
            difficulty=replay_info.difficulty,
            score=replay_info.score,
            category=models.Category.STANDARD,
            comment="Hello",
            video_link="",
            is_good=True,
            is_clear=True,
            no_bomb=False,
            miss_count=None,
            temp_replay_instance=temp_replay,
            replay_info=replay_info,
        )
        self.assertEqual(new_replay.scene_game_level, 11)
        self.assertEqual(new_replay.scene_game_scene, 2)

    def testPublishReplayIgnoresNoBombWhenNotApplicable(self):
        replay_file_contents = test_replays.GetRaw("th9_lunatic")

        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()

        replay_info = replay_parsing.Parse(replay_file_contents)

        new_replay = create_replay.PublishNewReplay(
            user=self.user,
            difficulty=3,
            score=49348230,
            category=models.Category.STANDARD,
            comment="",
            video_link="",
            is_good=True,
            is_clear=True,
            no_bomb=False,
            miss_count=None,
            temp_replay_instance=temp_replay,
            replay_info=replay_info,
        )

        self.assertIsNone(new_replay.no_bomb)

    def testPublishReplaySavesStages_TH10(self):
        replay_file_contents = test_replays.GetRaw("th10_normal")

        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()

        replay_info = replay_parsing.Parse(replay_file_contents)

        new_replay = create_replay.PublishNewReplay(
            user=self.user,
            difficulty=3,
            score=294127890,
            category=models.Category.STANDARD,
            comment="",
            video_link="",
            is_good=True,
            is_clear=True,
            no_bomb=False,
            miss_count=None,
            temp_replay_instance=temp_replay,
            replay_info=replay_info,
        )

        stages = list(models.ReplayStage.objects.filter(replay=new_replay))
        self.assertEqual(len(stages), 6)

        self.assertEqual(stages[0].score, 12996310)

    def testPublishReplaySavesStages_TH03(self):
        replay_file_contents = test_replays.GetRaw("th3_normal")
        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()
        replay_info = replay_parsing.Parse(replay_file_contents)

        new_replay = create_replay.PublishNewReplay(
            user=self.user,
            difficulty=replay_info.difficulty,
            score=replay_info.score,
            category=models.Category.STANDARD,
            comment="",
            video_link="",
            is_good=True,
            is_clear=False,
            no_bomb=None,
            miss_count=replay_info.miss_count,
            temp_replay_instance=temp_replay,
            replay_info=replay_info,
        )

        self.assertEqual(new_replay.shot.shot_id, "Reimu")
        self.assertTrue(new_replay.is_clear)
        self.assertEqual(new_replay.miss_count, 3)
        self.assertEqual(new_replay.slowdown, 2.5)
        self.assertIsNone(new_replay.no_bomb)
        stages = list(
            models.ReplayStage.objects.filter(replay=new_replay).select_related(
                "th03_opponent_shot"
            )
        )
        self.assertEqual(len(stages), 2)
        self.assertEqual(stages[0].score, 12_345_670)
        self.assertEqual(stages[0].th03_opponent_shot.shot_id, "Mima")
        self.assertEqual(stages[0].th03_opponent_score, 9_876_540)
        self.assertEqual(stages[0].lives, 3)
        self.assertEqual(stages[1].lives, 3)
        self.assertEqual(new_replay.th03_ruleset, 0)
        self.assertFalse(new_replay.th03_is_netplay)
        self.assertEqual(new_replay.th03_recorder_source, 3)
        self.assertIsNone(new_replay.th03_p1_uuid)
        self.assertIsNone(new_replay.th03_p1_name)

    def testPublishNetplayReplayKeepsIdentityAndLocalProjection_TH03(self):
        replay_file_contents = bytearray(test_replays.GetRaw("th3_pvp"))
        replay_file_contents[0x26F] = 1
        replay_file_contents[0x270] = 2
        replay_file_contents[0x271] = 2
        replay_file_contents[0x272:0x282] = bytes(range(1, 17))
        replay_file_contents[0x282:0x292] = bytes(range(17, 33))
        replay_file_contents[0x292:0x2A2] = bytes(range(33, 49))
        replay_file_contents[0x2A2] = len(b"Alice Example")
        replay_file_contents[0x2A3] = len(b"Bob")
        replay_file_contents[0x2A4 : 0x2A4 + len(b"Alice Example")] = b"Alice Example"
        replay_file_contents[0x2DD : 0x2DD + len(b"Bob")] = b"Bob"
        replay_file_contents = bytes(replay_file_contents)
        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()
        replay_info = replay_parsing.Parse(replay_file_contents)

        new_replay = create_replay.PublishNewReplay(
            user=self.user,
            difficulty=replay_info.difficulty,
            score=replay_info.score,
            category=models.Category.STANDARD,
            comment="",
            video_link="",
            is_good=True,
            is_clear=False,
            no_bomb=None,
            miss_count=None,
            temp_replay_instance=temp_replay,
            replay_info=replay_info,
        )
        new_replay.refresh_from_db()

        self.assertEqual(new_replay.shot.shot_id, "Yumemi")
        self.assertEqual(new_replay.rep_score, 98_765_430)
        self.assertTrue(new_replay.th03_is_netplay)
        self.assertEqual(new_replay.th03_recorder_role, 2)
        self.assertEqual(new_replay.th03_p1_name, "Alice Example")
        self.assertEqual(new_replay.th03_p2_name, "Bob")
        self.assertEqual(
            str(new_replay.th03_p1_uuid), "01020304-0506-0708-090a-0b0c0d0e0f10"
        )
        stage = models.ReplayStage.objects.select_related("th03_opponent_shot").get(
            replay=new_replay
        )
        self.assertEqual(stage.score, 98_765_430)
        self.assertEqual(stage.th03_opponent_shot.shot_id, "Reimu")
        self.assertEqual(stage.th03_opponent_score, 12_345_670)

        self.client.force_login(self.user)
        response = self.client.get(
            urls.reverse(
                "Replays/Details",
                kwargs={"game_id": game_ids.GameIDs.TH03, "replay_id": new_replay.id},
            )
        )
        self.assertContains(response, "Alice Example")
        self.assertContains(response, "Bob")
        self.assertContains(response, "Netplay?")
        self.assertNotContains(response, "Dopamine Arrange")
        self.assertContains(response, "Stock")

    def testPublishReplaySpellPractice(self):
        replay_file_contents = test_replays.GetRaw("th8_spell_practice")

        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()
        replay_info = replay_parsing.Parse(replay_file_contents)
        create_replay.PublishNewReplay(
            user=self.user,
            difficulty=replay_info.difficulty,
            score=replay_info.score,
            category=models.Category.STANDARD,
            comment="",
            video_link="",
            is_good=True,
            is_clear=True,
            no_bomb=None,
            miss_count=None,
            temp_replay_instance=temp_replay,
            replay_info=replay_info,
        )

    def testPublishReplayImportedUserName(self):
        replay_file_contents = test_replays.GetRaw("th10_normal")

        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()

        replay_info = replay_parsing.Parse(replay_file_contents)

        new_replay = create_replay.PublishNewReplay(
            user=None,
            difficulty=3,
            score=294127890,
            category=models.Category.STANDARD,
            comment="Hello",
            video_link="",
            is_good=True,
            is_clear=False,
            temp_replay_instance=temp_replay,
            replay_info=replay_info,
            no_bomb=False,
            miss_count=3,
            imported_username="あ",
        )

        self.assertEqual(new_replay.user, None)
        self.assertEqual(new_replay.imported_username, "あ")

    def testReplayDuplicates(self):
        replay_file_contents = test_replays.GetRaw("th10_normal")

        temp_replay_1 = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay_1.save()

        replay_info = replay_parsing.Parse(replay_file_contents)

        replay_1 = create_replay.PublishNewReplay(
            user=self.user,
            difficulty=3,
            score=12345,
            category=models.Category.STANDARD,
            comment="",
            video_link="",
            is_good=True,
            is_clear=True,
            no_bomb=False,
            miss_count=None,
            temp_replay_instance=temp_replay_1,
            replay_info=replay_info,
        )

        temp_replay_2 = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay_2.save()

        replay_info = replay_parsing.Parse(replay_file_contents)

        with self.assertRaises(utils.IntegrityError):
            create_replay.PublishNewReplay(
                user=self.user,
                difficulty=3,
                score=67890,
                category=models.Category.STANDARD,
                comment="",
                video_link="",
                is_good=True,
                is_clear=True,
                no_bomb=False,
                miss_count=None,
                temp_replay_instance=temp_replay_2,
                replay_info=replay_info,
            )

        self.assertEqual(
            constant_helpers.GetReplayFileWithSameHash(replay_file_contents).replay,
            replay_1,
        )
        with self.assertRaises(models.Replay.DoesNotExist):
            models.Replay.objects.get(score=67890)

    def testReplayDuplicateFromRoyalFlare(self):
        test_replays.CreateAsPublishedReplay("th6_extra", imported_username="someone")

        replay_file_contents = test_replays.GetRaw("th6_extra")
        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()
        replay_info = replay_parsing.Parse(replay_file_contents)

        with self.assertRaises(utils.IntegrityError):
            create_replay.PublishNewReplay(
                user=self.user,
                difficulty=3,
                score=1234567,
                category=models.Category.STANDARD,
                comment="",
                video_link="",
                is_good=True,
                is_clear=True,
                no_bomb=False,
                miss_count=None,
                temp_replay_instance=temp_replay,
                replay_info=replay_info,
            )

    def testReplayDuplicates_DeletesGhosts(self):
        inactive_user = self.createUser("inactive")

        ghost = test_replays.CreateAsPublishedReplay("th6_extra", user=inactive_user)
        inactive_user.MarkForDeletion()

        replay_file_contents = test_replays.GetRaw("th6_extra")
        temp_replay = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents
        )
        temp_replay.save()
        replay_info = replay_parsing.Parse(replay_file_contents)

        create_replay.PublishNewReplay(
            user=self.user,
            difficulty=3,
            score=1234567,
            category=models.Category.STANDARD,
            comment="",
            video_link="",
            is_good=True,
            is_clear=True,
            no_bomb=False,
            miss_count=None,
            temp_replay_instance=temp_replay,
            replay_info=replay_info,
        )
        # No duplicate error.

        with self.assertRaises(models.Replay.DoesNotExist):
            models.Replay.objects.get(id=ghost.pk)

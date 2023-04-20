import logging
from replays.management.commands.delete_imported_replays import delete_imported_replays
from replays.create_replay import PublishNewReplay
from replays.test_replay_parsing import ParseTestReplay
from replays import models
from replays.testing import test_case
from replays.testing import test_replays


class DeleteImportedReplaysTest(test_case.ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.createUser("some-user")

    def testDeleteImportedReplays(self):
        replay_info_1 = ParseTestReplay("th6_hard_1cc")
        replay_file_contents_1 = test_replays.GetRaw("th10_normal")
        temp_replay_1 = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents_1
        )
        temp_replay_1.save()
        PublishNewReplay(
            user=self.user,
            difficulty=0,
            score=1_000_000,
            category=0,
            comment="鼻毛",
            video_link="",
            temp_replay_instance=temp_replay_1,
            is_good=True,
            is_clear=True,
            no_bomb=False,
            miss_count=None,
            replay_info=replay_info_1,
        )

        replay_info_2 = ParseTestReplay("th16_extra")
        replay_file_contents_2 = test_replays.GetRaw("th16_extra")
        temp_replay_2 = models.TemporaryReplayFile(
            user=None, replay=replay_file_contents_2
        )
        temp_replay_2.save()
        PublishNewReplay(
            user=None,
            difficulty=0,
            score=2_000_000,
            category=0,
            comment="Comment",
            video_link="",
            temp_replay_instance=temp_replay_2,
            is_good=True,
            is_clear=True,
            no_bomb=False,
            miss_count=None,
            replay_info=replay_info_2,
            imported_username="あ",
        )

        all_replays_before = models.Replay.objects.all()
        self.assertEqual(len(all_replays_before), 2)

        with self.assertLogs(logging.getLogger(), level="INFO"):
            delete_imported_replays()

        all_replays_after = models.Replay.objects.all()
        self.assertEquals(len(all_replays_after), 1)
        self.assertIsNone(all_replays_after[0].imported_username)

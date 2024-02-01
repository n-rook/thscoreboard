import datetime
from unittest.mock import patch

from replays.testing import test_case
from replays.replays_to_json import ReplayToJsonConverter, create_leaderboard_url
from replays.test_replay_parsing import ParseTestReplay
from replays.create_replay import PublishNewReplay
from replays import models
from replays.testing import test_replays
from replays.testing import test_utilities


class ReplaysToJsonTestCase(test_case.ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.createUser("some-user")

    def testConvertReplaysToJsonString(self):
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
            category=models.Category.STANDARD,
            comment="鼻毛",
            video_link="",
            temp_replay_instance=temp_replay_1,
            is_good=True,
            is_clear=True,
            no_bomb=False,
            miss_count=None,
            replay_info=replay_info_1,
            created_timestamp=datetime.datetime(
                2000, 1, 1, tzinfo=datetime.timezone.utc
            ),
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
            score=0,
            category=models.Category.STANDARD,
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

        replays = models.Replay.objects.order_by("-score").annotate_with_rank()

        with test_utilities.OverrideTranslations():
            converter = ReplayToJsonConverter()
            json_data = [converter.convert_replay_to_dict(replay) for replay in replays]

        for json_replay_data in json_data:
            assert json_replay_data
            assert isinstance(json_replay_data["Score"], dict)
            assert set(json_replay_data["Score"].keys()) == {"text", "url"}

            assert isinstance(json_replay_data["Replay"], dict)
            assert set(json_replay_data["Replay"].keys()) == {"text", "url"}

        assert json_data[0]["User"]["text"] == self.user.username
        assert json_data[0]["User"]["url"] == f"/replays/user/{self.user.username}"
        assert json_data[0]["Game"]["text"] == "th06"
        assert json_data[0]["Game"]["url"] == "/replays/th06"
        assert json_data[0]["Difficulty"]["text"] == "Easy"
        assert json_data[0]["Difficulty"]["url"] == "/replays/th06?difficulty=0"
        assert json_data[0]["Shot"]["text"] == "Reimu A"
        assert json_data[0]["Shot"]["url"] == "/replays/th06?difficulty=0&shot=ReimuA"
        assert json_data[0]["Score"]["text"] == "🥇1,000,000"
        assert json_data[0]["Upload Date"] == "2000-01-01"
        assert json_data[0]["Comment"] == "鼻毛"
        assert json_data[0]["Replay"]["text"] == "⬇"
        assert "Character" not in json_data[0]["Replay"]["text"]
        assert "Season" not in json_data[0]["Replay"]["text"]

        assert json_data[1]["User"] == "あ"
        assert json_data[1]["Character"] == "Marisa"
        assert json_data[1]["Subshot"] is None

    def testMedalEmojisSingleShot(self):
        for i in range(5):
            with patch(
                "replays.constant_helpers.CalculateReplayFileHash"
            ) as mocked_hash:
                mocked_hash.return_value = bytes(i)
                test_replays.CreateAsPublishedReplay(
                    "th10_normal",
                    user=self.user,
                    score=1_000_000_000 - 100_000_000 * i,
                    difficulty=0,
                )

        replays = models.Replay.objects.order_by("-score").annotate_with_rank()
        with test_utilities.OverrideTranslations():
            converter = ReplayToJsonConverter()
            json_data = [converter.convert_replay_to_dict(replay) for replay in replays]

        self.assertEquals(json_data[0]["Score"]["text"], "🥇1,000,000,000")
        self.assertEquals(json_data[1]["Score"]["text"], "🥈900,000,000")
        self.assertEquals(json_data[2]["Score"]["text"], "🥉800,000,000")
        self.assertEquals(json_data[3]["Score"]["text"], "700,000,000")
        self.assertEquals(json_data[4]["Score"]["text"], "600,000,000")

    def testMedalEmojisMultipleShots(self):
        replay_filenames = [
            "th10_normal",
            "th11_normal",
        ]
        for i, filename in enumerate(replay_filenames):
            test_replays.CreateAsPublishedReplay(
                filename,
                user=self.user,
                score=1_000_000_000 - 100_000_000 * i,
                difficulty=0,
            )

        replays = models.Replay.objects.order_by("-score").annotate_with_rank()

        with test_utilities.OverrideTranslations():
            converter = ReplayToJsonConverter()
            json_data = [converter.convert_replay_to_dict(replay) for replay in replays]

        self.assertEquals(json_data[0]["Score"]["text"], "🥇1,000,000,000")
        self.assertEquals(json_data[1]["Score"]["text"], "🥇900,000,000")

    def testCreateLeaderboardUrlWithUrlEncoding(self) -> None:
        actual = create_leaderboard_url(
            game_id="th08",
            difficulty_id=1,
            shot_id="Reimu & Yukari",
            route_id="Final A",
        )
        expected = (
            "/replays/th08?difficulty=1&shot=Reimu%20%26%20Yukari&route=Final%20A"
        )
        self.assertEquals(actual, expected)

    def testCreateLeaderboardUrlWithoutOptionalFields(self) -> None:
        actual = create_leaderboard_url(
            game_id="th08",
            difficulty_id=1,
        )
        expected = "/replays/th08?difficulty=1"
        self.assertEquals(actual, expected)

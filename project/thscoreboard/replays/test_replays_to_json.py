import datetime
from replays.testing import test_case
from replays.replays_to_json import ReplayToJsonConverter
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
        replay_1 = PublishNewReplay(
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
        replay_2 = PublishNewReplay(
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

        replays = [replay_1, replay_2]

        with test_utilities.OverrideTranslations():
            converter = ReplayToJsonConverter()
            json_data = converter.convert_replays_to_serializable_list(replays)

        assert len(json_data) == len(replays)

        for replay, json_replay_data in zip(replays, json_data):
            assert json_replay_data
            assert type(json_replay_data["Score"]) == dict
            assert set(json_replay_data["Score"].keys()) == {"text", "url"}

            assert type(json_replay_data["Replay"]) == dict
            assert set(json_replay_data["Replay"].keys()) == {"text", "url"}

        assert json_data[0]["User"]["text"] == self.user.username
        assert json_data[0]["User"]["url"] == f"/replays/user/{self.user.username}"
        assert json_data[0]["Game"] == "th06"
        assert json_data[0]["Difficulty"] == "Easy"
        assert json_data[0]["Shot"] == "Reimu A"
        assert json_data[0]["Score"]["text"] == "1,000,000"
        assert json_data[0]["Upload Date"] == "2000-01-01"
        assert json_data[0]["Comment"] == "鼻毛"
        assert json_data[0]["Replay"]["text"] == "⬇"
        assert "Character" not in json_data[0]["Replay"]["text"]
        assert "Season" not in json_data[0]["Replay"]["text"]

        assert json_data[1]["User"] == "あ"
        assert json_data[1]["Character"] == "Marisa"
        assert json_data[1]["Season"] is None

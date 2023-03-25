from replays.testing import test_case
from replays.replays_to_json import convert_replays_to_serializable_list
from replays.test_replay_parsing import ParseTestReplay
from replays.create_replay import PublishNewReplay
from replays import models
from replays.testing import test_replays


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
            comment="Comment",
            video_link="",
            temp_replay_instance=temp_replay_1,
            is_good=True,
            is_clear=True,
            replay_info=replay_info_1,
        )

        replay_info_2 = ParseTestReplay("th16_extra")
        replay_file_contents_2 = test_replays.GetRaw("th16_extra")
        temp_replay_2 = models.TemporaryReplayFile(
            user=self.user, replay=replay_file_contents_2
        )
        temp_replay_2.save()
        replay_2 = PublishNewReplay(
            user=self.user,
            difficulty=0,
            score=2_000_000,
            category=0,
            comment="Comment",
            video_link="",
            temp_replay_instance=temp_replay_2,
            is_good=True,
            is_clear=True,
            replay_info=replay_info_2,
        )

        replays = [replay_1, replay_2]

        json_data = convert_replays_to_serializable_list(replays)

        assert len(json_data) == len(replays)

        for replay, json_replay_data in zip(replays, json_data):
            assert json_replay_data
            assert set(json_replay_data.keys()) == {
                "Id",
                "User",
                "Game",
                "Difficulty",
                "Shot",
                "Score",
                "Upload Date",
                "Replay",
            }
            assert json_replay_data["User"]["text"] == self.user.username
            assert json_replay_data["Game"] == replay.shot.game.GetShortName()

            assert type(json_replay_data["Score"]) == dict
            assert set(json_replay_data["Score"].keys()) == {"text", "url"}

            assert type(json_replay_data["Replay"]) == dict
            assert set(json_replay_data["Replay"].keys()) == {"text", "url"}

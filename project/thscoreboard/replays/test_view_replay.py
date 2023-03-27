from replays import replay_parsing
from replays.testing import test_case
from replays.testing import test_replays

from . import game_ids
from . import game_fields


tests = [
    (game_ids.GameIDs.TH06, "th6_hard_1cc"),
    (game_ids.GameIDs.TH07, "th7_lunatic"),
    (game_ids.GameIDs.TH10, "th10_normal"),
    (game_ids.GameIDs.TH11, "th11_normal"),
    (game_ids.GameIDs.TH06, "th6_extra"),
    (game_ids.GameIDs.TH08, "th8_normal"),
    (game_ids.GameIDs.TH08, "th8_extra"),
    (game_ids.GameIDs.TH08, "th8_spell_practice"),
]


class TestTableFields(test_case.ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.createUser("view-replay-user")

    def testFields(self):
        for gameid, file in tests:
            with self.subTest(gameid=gameid, file=file):
                rpy = test_replays.GetRaw(file)
                replay_info = replay_parsing.Parse(rpy)
                fields = game_fields.GetGameField(gameid, replay_info.replay_type)
                for key in fields:
                    for i, s in enumerate(replay_info.stages):
                        if i < len(replay_info.stages) - 1:
                            # don't test last stage coz fields might be missing
                            if fields[key]:
                                self.assertIsNotNone(
                                    s[key], msg=f"Expected field {key} not found"
                                )
                            if not fields[key]:
                                """games with varying life piece threshholds cannot have them hardcoded
                                so the life pieces column needs to be visible for them, but not visible for those with static threshholds

                                update: both life pieces and bomb pieces have been merged into the lives and bombs field
                                so they're now removed from the frontend and aren't relevant anymore
                                """
                                self.assertIsNone(
                                    s[key], msg=f"Unexpected field {key} found"
                                )

from replays import game_ids
from replays import constant_helpers
from replays import replay_parsing
from replays.testing import test_case
from replays.testing import test_replays


class ConstantHelpersTest(test_case.ReplayTestCase):
    def setUp(self):
        super().setUp()
        self.user = self.createUser("some-user")

    def testGetWithoutRoute(self):
        replay_file_contents = test_replays.GetRaw("th10_normal")
        replay_info = replay_parsing.Parse(replay_file_contents)
        constants = constant_helpers.GetModelInstancesForReplay(replay_info)

        self.assertEqual(constants.game.game_id, game_ids.GameIDs.TH10)
        self.assertEqual(constants.shot.shot_id, "ReimuB")
        self.assertIsNone(constants.route)

    def testGetWithRoute(self):
        replay_file_contents = test_replays.GetRaw("th8_normal")
        replay_info = replay_parsing.Parse(replay_file_contents)
        constants = constant_helpers.GetModelInstancesForReplay(replay_info)

        self.assertEqual(constants.game.game_id, game_ids.GameIDs.TH08)
        self.assertEqual(constants.shot.shot_id, "Yukari")
        self.assertIsNotNone(constants.route)
        self.assertEqual(constants.route.route_id, "Final B")

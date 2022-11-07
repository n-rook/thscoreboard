from replays import replay_parsing
from replays.testing import test_case
from replays.testing import test_replays

from . import game_ids
from . import game_fields

import logging


tests = [
    (game_ids.GameIDs.TH06, 'th6_hard_1cc'),
    (game_ids.GameIDs.TH07, 'th7_lunatic'),
    (game_ids.GameIDs.TH10, 'th10_normal'),
    (game_ids.GameIDs.TH11, 'th11_normal')
]


class TestTableFields(test_case.ReplayTestCase):

    def setUp(self):
        super().setUp()
        self.user = self.createUser('view-replay-user')

    def testFields(self):
        for gameid, file in tests:
            logging.info('testing game fields %s %s', gameid, file)
            rpy = test_replays.GetRaw(file)
            replay_info = replay_parsing.Parse(rpy)
            fields = game_fields.GetGameField(gameid)
            for key in fields:
                logging.info(key)
                logging.info(fields[key])
                for s in replay_info.stages:
                    if fields[key]:
                        self.assertIsNotNone(s[key])
                    if not fields[key]:
                        self.assertIsNone(s[key])


class TestGetPower(test_case.ReplayTestCase):

    def testGetPower(self):
        self.assertEqual(game_fields.GetPowerFormat(game_ids.GameIDs.TH06, 100), '100')
        self.assertEqual(game_fields.GetPowerFormat(game_ids.GameIDs.TH07, 100), '100')
        self.assertEqual(game_fields.GetPowerFormat(game_ids.GameIDs.TH10, 100), '5.00')
        self.assertEqual(game_fields.GetPowerFormat(game_ids.GameIDs.TH10, 66), '3.30')

    def testGetLivesFormat(self):
        self.assertEqual(game_fields.GetLivesFormat(game_ids.GameIDs.TH11, 5, 2), '5 (2/5)')

from os import path

from replays import replay_parsing
from replays.testing import test_case

from . import game_ids
from . import game_fields

import logging


def ReadTestFile(filename):
    with open(path.join('replays/replays_for_tests', filename), 'rb') as f:
        return f.read()


tests = [
    (game_ids.GameIDs.TH06, 'th6_hard_1cc.rpy'),
    (game_ids.GameIDs.TH07, 'th7_lunatic.rpy'),
    (game_ids.GameIDs.TH10, 'th10_normal.rpy')
]


class TestTableFields(test_case.ReplayTestCase):

    def setUp(self):
        super().setUp()
        self.user = self.createUser('view-replay-user')

    def testFields(self):
        for gameid, file in tests:
            logging.info('testing game fields %s %s', gameid, file)
            rpy = ReadTestFile(file)
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

from replays import replay_parsing
from replays.testing import test_case
from replays.testing import test_replays

from . import game_ids
from . import game_fields


tests = [
    (game_ids.GameIDs.TH06, 'th6_hard_1cc'),
    (game_ids.GameIDs.TH07, 'th7_lunatic'),
    (game_ids.GameIDs.TH10, 'th10_normal'),
    (game_ids.GameIDs.TH11, 'th11_normal'),
    (game_ids.GameIDs.TH06, 'th6_extra'),
    (game_ids.GameIDs.TH08, 'th8_normal'),
    (game_ids.GameIDs.TH08, 'th8_extra'),
    (game_ids.GameIDs.TH08, 'th8_spell_practice'),
]


class TestTableFields(test_case.ReplayTestCase):

    def setUp(self):
        super().setUp()
        self.user = self.createUser('view-replay-user')

    def testFields(self):
        for gameid, file in tests:
            with self.subTest(gameid=gameid, file=file):
                rpy = test_replays.GetRaw(file)
                replay_info = replay_parsing.Parse(rpy)
                fields = game_fields.GetGameField(gameid)
                for key in fields:
                    for (i, s) in enumerate(replay_info.stages):
                        if i < len(replay_info.stages) - 1:
                            # don't test last stage coz fields might be missing
                            if fields[key]:
                                self.assertIsNotNone(s[key], msg=f'Expected field {key} not found')
                            if not fields[key]:
                                self.assertIsNone(s[key], msg=f'Unexpected field {key} found')


class TestGetPower(test_case.ReplayTestCase):

    def testGetPower(self):
        self.assertEqual(game_fields.GetFormatPower(game_ids.GameIDs.TH06, 100), '100')
        self.assertEqual(game_fields.GetFormatPower(game_ids.GameIDs.TH07, 100), '100')
        self.assertEqual(game_fields.GetFormatPower(game_ids.GameIDs.TH10, 100), '5.00')
        self.assertEqual(game_fields.GetFormatPower(game_ids.GameIDs.TH10, 66), '3.30')

    def testGetFormatLives(self):

        self.assertEqual(game_fields.GetFormatLives(game_ids.GameIDs.TH11, 5, 2), '5 (2/5)')
        self.assertEqual(game_fields.GetFormatLives(game_ids.GameIDs.TH10, 5, 2), '5')

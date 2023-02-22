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
                fields = game_fields.GetGameField(gameid, replay_info.replay_type)
                for key in fields:
                    for (i, s) in enumerate(replay_info.stages):
                        if i < len(replay_info.stages) - 1:
                            # don't test last stage coz fields might be missing
                            if fields[key]:
                                self.assertIsNotNone(s[key], msg=f'Expected field {key} not found')
                            if not fields[key]:
                                """games with varying life piece threshholds cannot have them hardcoded
                                so the life pieces column needs to be visible for them, but not visible for those with static threshholds
                                
                                update: both life pieces and bomb pieces have been merged into the lives and bombs field
                                so they're now removed from the frontend and aren't relevant anymore
                                """
                                self.assertIsNone(s[key], msg=f'Unexpected field {key} found')


class TestGameFields(test_case.ReplayTestCase):

    def testGetPower(self):
        self.assertEqual(game_fields.GetFormatPower(game_ids.GameIDs.TH06, 100), '100')
        self.assertEqual(game_fields.GetFormatPower(game_ids.GameIDs.TH07, 100), '100')
        self.assertEqual(game_fields.GetFormatPower(game_ids.GameIDs.TH10, 100), '5.00')
        self.assertEqual(game_fields.GetFormatPower(game_ids.GameIDs.TH10, 66), '3.30')

    def testGetFormatLives(self):

        self.assertEqual(game_fields.GetFormatLives(game_ids.GameIDs.TH11, 5, 2), '5 (2/5)')
        self.assertEqual(game_fields.GetFormatLives(game_ids.GameIDs.TH10, 5, 2), '5')

    def testGetFormatLifePieces(self):
        self.assertEqual(game_fields.GetFormatLives(game_ids.GameIDs.TH13, 2, 3, 0), '2 (3/8)')
        self.assertEqual(game_fields.GetFormatLives(game_ids.GameIDs.TH13, 5, 7, 3), '5 (7/15)')
        self.assertEqual(game_fields.GetFormatLives(game_ids.GameIDs.TH13, 8, 1, 9), '8 (1/25)')
        self.assertEqual(game_fields.GetFormatLives(game_ids.GameIDs.TH13, None, None, 0), None)

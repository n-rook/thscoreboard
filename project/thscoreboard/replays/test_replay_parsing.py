import unittest

from replays.testing import test_replays
from replays import replay_parsing
from replays import game_fields
from replays import game_ids


def ParseTestReplay(filename):
    return replay_parsing.Parse(test_replays.GetRaw(filename))


class Th06ReplayTestCase(unittest.TestCase):
    
    def testHard1cc(self):
        r = ParseTestReplay('th6_hard_1cc')
        self.assertEqual(r.game, 'th06')
        self.assertEqual(r.difficulty, 2)
        self.assertEqual(r.shot, 'ReimuA')
        self.assertEqual(r.score, 92245410)
        self.assertEqual(r.name, 'nrook   ')
        self.assertEqual(r.replay_type, game_ids.ReplayTypes.REGULAR)

        self.assertEqual(r.stages[0].stage, 0)
        self.assertEqual(r.stages[0].score, 5204570)
        self.assertEqual(r.stages[0].lives, 2)
        self.assertEqual(r.stages[0].th06_rank, 26)

        self.assertEqual(r.stages[5].stage, 5)
        self.assertEqual(r.stages[5].score, 92245410)
        self.assertEqual(r.stages[5].power, None)
        self.assertEqual(r.stages[5].lives, None)
        self.assertEqual(r.stages[5].bombs, None)
        self.assertEqual(r.stages[5].th06_rank, None)

        # 6 stages (Hard 1cc)
        # Final score is 92245410
        # Final resources are 0 lives, 2 bombs

    def testExtra(self):
        r = ParseTestReplay('th6_extra')
        self.assertEqual(r.game, 'th06')
        self.assertEqual(r.difficulty, 4)
        self.assertEqual(r.shot, 'MarisaA')
        self.assertEqual(r.score, 181144360)
        self.assertEqual(r.name, 'AAAAAAAA')
        self.assertEqual(r.replay_type, game_ids.ReplayTypes.REGULAR)

        self.assertEqual(r.stages[0].stage, 6)
        self.assertEqual(r.stages[0].score, 181144360)
        self.assertEqual(r.stages[0].power, None)
        self.assertEqual(r.stages[0].lives, None)
        self.assertEqual(r.stages[0].bombs, None)
        self.assertEqual(r.stages[0].th06_rank, None)


class Th07ReplayTestCase(unittest.TestCase):

    def testLunatic(self):
        r = ParseTestReplay('th7_lunatic')
        self.assertEqual(r.game, 'th07')
        self.assertEqual(r.difficulty, 3)
        self.assertEqual(r.shot, "SakuyaB")
        self.assertEqual(r.score, 702864100)
        self.assertEqual(r.name, 'AAAAAAAA')

    def testStages(self):
        r = ParseTestReplay('th7_lunatic')

        self.assertEqual(len(r.stages), 6)
        self.assertEqual(r.replay_type, 1)
        stage_2 = r.stages[1]
        self.assertEqual(stage_2.score, 68342530)
        self.assertEqual(stage_2.piv, 343790)
        self.assertEqual(stage_2.graze, 868)
        self.assertEqual(stage_2.power, 128)
        self.assertEqual(stage_2.lives, 3)
        self.assertEqual(stage_2.bombs, 4)
        self.assertIsNone(stage_2.th06_rank)
        self.assertEqual(stage_2.th07_cherry, 8400)
        self.assertEqual(stage_2.th07_cherrymax, 345160)

    def testExtraData(self):
        ParseTestReplay('th7_extra_data')


class Th08ReplayTestCase(unittest.TestCase):

    def testNormal(self):
        r = ParseTestReplay('th8_normal')

        self.assertEqual(len(r.stages), 6)
        self.assertEqual(r.name, 'AAAAAAAA')
        self.assertEqual(r.shot, 'Yukari')
        self.assertEqual(r.score, 1240093320)
        self.assertEqual(r.difficulty, 1)

        self.assertEqual(r.stages[0].score, 37008330)
        self.assertEqual(r.stages[0].power, 113)
        self.assertEqual(r.stages[0].point_items, 58)
        self.assertEqual(r.stages[0].lives, 2)
        self.assertEqual(r.stages[0].th07_cherry, None)
        self.assertEqual(r.stages[0].th07_cherrymax, None)

        self.assertEqual(r.stages[3].stage, 4)
        self.assertEqual(r.stages[5].stage, 7)
        self.assertEqual(game_fields.GetFormatStage(r.game, r.stages[3].stage), '4B')
        self.assertEqual(game_fields.GetFormatStage(r.game, r.stages[5].stage), '6B')

    def testExtra(self):
        r = ParseTestReplay('th8_extra')

        self.assertEqual(len(r.stages), 1)
        self.assertEqual(r.name, 'AAAAAAAA')
        self.assertEqual(r.shot, 'Marisa & Alice')
        self.assertEqual(r.score, 1213587810)

        self.assertEqual(r.stages[0].score, 1213587810)
        self.assertEqual(r.stages[0].piv, None)
        self.assertEqual(r.replay_type, 1)

    def testLzss(self):
        ParseTestReplay('th8_lzss')

    def testSpellPractice(self):
        r = ParseTestReplay('th8_spell_practice')
        self.assertEqual(len(r.stages), 0)
        self.assertEqual(r.spell_card_id, 215)
        self.assertEqual(r.spell_card_id_format, 216)
        self.assertEqual(r.difficulty, 1)
        self.assertEqual(r.replay_type, game_ids.ReplayTypes.SPELL_PRACTICE)

        r = ParseTestReplay('th8_spell_practice_2')
        self.assertEqual(r.spell_card_id, 34)
        self.assertEqual(r.spell_card_id_format, 35)
        self.assertEqual(r.difficulty, 2)
        self.assertEqual(r.replay_type, game_ids.ReplayTypes.SPELL_PRACTICE)


class Th09ReplayTestCase(unittest.TestCase):
    
    def testLunatic(self):
        r = ParseTestReplay('th9_lunatic')

        self.assertEqual(r.difficulty, 3)
        self.assertEqual(r.shot, 'Reimu')
        self.assertEqual(r.score, 49348230)
        self.assertEqual(r.name, 'AAAAAAAA')
        self.assertEqual(r.replay_type, game_ids.ReplayTypes.REGULAR)

        s = r.stages[8]

        self.assertEqual(s.score, None)
        self.assertEqual(s.lives, None)
        self.assertEqual(s.th09_p2_cpu, True)
        self.assertEqual(s.th09_p2_shot, 'Eiki')
        self.assertEqual(s.th09_p2_score, None)

    def testPVP(self):
        r = ParseTestReplay('th9_pvp')

        self.assertEqual(r.difficulty, 3)
        self.assertEqual(r.shot, 'Yuuka')
        self.assertEqual(r.score, 0)
        self.assertEqual(r.name, '17:49:20')
        self.assertEqual(r.replay_type, game_ids.ReplayTypes.PVP)

        s = r.stages[0]

        self.assertEqual(s.score, 0)
        self.assertEqual(s.th09_p1_cpu, False)
        self.assertEqual(s.th09_p2_cpu, False)
        self.assertEqual(s.th09_p2_shot, 'Lunasa')
        self.assertEqual(s.th09_p2_score, 0)


class Th10ReplayTestCase(unittest.TestCase):
    
    def testNormal(self):
        r = ParseTestReplay('th10_normal')
        self.assertEqual(r.game, 'th10')
        self.assertEqual(r.difficulty, 1)
        self.assertEqual(r.shot, 'ReimuB')
        self.assertEqual(r.score, 294127890)
        self.assertEqual(r.name, 'AAAAAAAA')
        self.assertEqual(r.stages[1].piv, 159660)
        
    def testNull(self):
        with self.assertRaises(replay_parsing.BadReplayError):
            ParseTestReplay('th10_null')

    def testSmall(self):
        with self.assertRaises(replay_parsing.BadReplayError):
            ParseTestReplay('th10_small')

    def testStagePractice(self):
        r = ParseTestReplay('th10_stage_practice')
        self.assertEqual(r.replay_type, game_ids.ReplayTypes.STAGE_PRACTICE)


class Th11ReplayTestCase(unittest.TestCase):

    def testNormal(self):
        r = ParseTestReplay('th11_normal')
        self.assertEqual(r.game, 'th11')
        self.assertEqual(r.difficulty, 1)
        self.assertEqual(r.score, 210042730)
        self.assertEqual(r.shot, "ReimuB")
        self.assertEqual(r.name, 'AAAAAAAA')
        self.assertEqual(r.replay_type, REGULAR)

        stage5 = r.stages[4]
        self.assertEqual(stage5.score, 92478530)
        self.assertEqual(stage5.power, 63)
        self.assertEqual(stage5.piv, 50040)
        self.assertEqual(stage5.lives, 5)
        self.assertEqual(stage5.life_pieces, 2)
        self.assertEqual(stage5.graze, 2820)


class Th12ReplayTestCase(unittest.TestCase):

    def testNormal(self):
        r = ParseTestReplay('th12_normal')
        self.assertEqual(r.game, 'th12')
        self.assertEqual(r.difficulty, 1)
        self.assertEqual(r.score, 168919360)
        self.assertEqual(r.shot, 'ReimuB')
        self.assertEqual(r.name, 'AAAAAAAA')
        self.assertEqual(r.replay_type, REGULAR)

        stage4end = r.stages[3]
        self.assertEqual(stage4end.score, 94202540)
        self.assertEqual(stage4end.piv, 13100)
        self.assertEqual(stage4end.life_pieces, 3)
        self.assertEqual(game_fields.GetFormatPower('th12', stage4end.power), '4.00')

    def testExtra(self):
        r = ParseTestReplay('th12_extra')
        self.assertEqual(r.game, 'th12')
        self.assertEqual(r.difficulty, 4)
        self.assertEqual(r.shot, 'SanaeB')
        self.assertEqual(r.score, 131238030)

        stage = r.stages[0]
        self.assertEqual(stage.score, 131238030)
        self.assertIsNone(stage.power)
        self.assertIsNone(stage.piv)
        self.assertIsNone(stage.lives)
        self.assertIsNone(stage.bomb_pieces)

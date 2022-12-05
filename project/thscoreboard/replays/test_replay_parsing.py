import unittest

from replays.testing import test_replays
from replays import replay_parsing
from replays import game_fields


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

        self.assertEqual(r.stages[0].stage, 0)
        self.assertEqual(r.stages[0].score, 5204570)
        self.assertEqual(r.stages[0].lives, 2)
        self.assertEqual(r.stages[0].th06_rank, 16)

        self.assertEqual(r.stages[5].stage, 5)
        self.assertEqual(r.stages[5].score, 92245410)
        self.assertEqual(r.stages[5].power, 128)
        self.assertEqual(r.stages[5].lives, 3)
        self.assertEqual(r.stages[5].bombs, 1)
        self.assertEqual(r.stages[5].th06_rank, 19)

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

        self.assertEqual(r.stages[0].stage, 6)
        self.assertEqual(r.stages[0].score, 181144360)
        self.assertEqual(r.stages[0].power, 0)
        self.assertEqual(r.stages[0].lives, 2)
        self.assertEqual(r.stages[0].bombs, 3)
        self.assertEqual(r.stages[0].th06_rank, 16)


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
        stage_2 = r.stages[1]
        self.assertEqual(stage_2.score, 68342530)
        self.assertEqual(stage_2.piv, 92800)
        self.assertEqual(stage_2.graze, 374)
        self.assertEqual(stage_2.power, 113)
        self.assertEqual(stage_2.lives, 2)
        self.assertEqual(stage_2.bombs, 4)
        self.assertIsNone(stage_2.th06_rank)
        self.assertEqual(stage_2.th07_cherry, 29080)
        self.assertEqual(stage_2.th07_cherrymax, 311380)


class Th08ReplayTestCase(unittest.TestCase):

    def testNormal(self):
        r = ParseTestReplay('th8_normal')

        self.assertEqual(len(r.stages), 6)
        self.assertEqual(r.name, 'AAAAAAAA')
        self.assertEqual(r.shot, 'Yukari')
        self.assertEqual(r.score, 1240093320)
        self.assertEqual(r.difficulty, 1)

        self.assertEqual(r.stages[0].score, 37008330)
        self.assertEqual(r.stages[0].power, 0)
        self.assertEqual(r.stages[0].point_items, 0)
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
        self.assertEqual(r.stages[0].piv, 300000)


class Th10ReplayTestCase(unittest.TestCase):
    
    def testNormal(self):
        r = ParseTestReplay('th10_normal')
        self.assertEqual(r.game, 'th10')
        self.assertEqual(r.difficulty, 1)
        self.assertEqual(r.shot, 'ReimuB')
        self.assertEqual(r.score, 294127890)
        self.assertEqual(r.name, 'AAAAAAAA')


class Th11ReplayTestCaseA(unittest.TestCase):

    def testNormal(self):
        r = ParseTestReplay('th11_normal')
        self.assertEqual(r.game, 'th11')
        self.assertEqual(r.difficulty, 1)
        self.assertEqual(r.score, 210042730)
        self.assertEqual(r.shot, "ReimuB")
        self.assertEqual(r.name, 'AAAAAAAA')

        stage5 = r.stages[4]
        self.assertEqual(stage5.score, 59938190)
        self.assertEqual(stage5.power, 80)
        self.assertEqual(stage5.piv, 66460)
        self.assertEqual(stage5.lives, 8)
        self.assertEqual(stage5.life_pieces, 1)
        self.assertEqual(stage5.graze, 1582)

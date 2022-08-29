from os import path
import unittest

from . import replay_parsing


def ParseTestReplay(filename):
    with open(path.join('scores/replays_for_tests', filename), 'rb') as f:
        return replay_parsing.Parse(f.read())


class Th06ReplayTestCase(unittest.TestCase):
    
    def testHard1cc(self):
        replay_info = ParseTestReplay('th6_hard_1cc.rpy')
        self.assertEqual(replay_info.game, 'th06')
        self.assertEqual(replay_info.difficulty, 2)
        self.assertEqual(replay_info.shot, 'ReimuA')
        self.assertEqual(replay_info.score, 92245410)

        # 6 stages (Hard 1cc)
        # Final score is 92245410
        # Final resources are 0 lives, 2 bombs

    def testExtra(self):
        replay_info = ParseTestReplay('th6_extra.rpy')
        self.assertEqual(replay_info.game, 'th06')
        self.assertEqual(replay_info.difficulty, 4)
        self.assertEqual(replay_info.shot, 'MarisaA')
        self.assertEqual(replay_info.score, 181144360)


class Th07ReplayTestCase(unittest.TestCase):

    def testLunatic(self):
        rpy = ParseTestReplay('th7_lunatic.rpy')
        self.assertEqual(rpy.game, 'th07')
        self.assertEqual(rpy.difficulty, 3)
        self.assertEqual(rpy.shot, "SakuyaB")
        self.assertEqual(rpy.score, 702864100)


class Th10ReplayTestCase(unittest.TestCase):
    
    def testNormal(self):
        rpy = ParseTestReplay('th10_normal.rpy')
        self.assertEqual(rpy.game, 'th10')
        self.assertEqual(rpy.difficulty, 1)
        self.assertEqual(rpy.shot, 'ReimuB')
        self.assertEqual(rpy.score, 294127890)

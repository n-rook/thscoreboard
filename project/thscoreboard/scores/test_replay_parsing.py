from os import path
import unittest

from . import replay_parsing


class Th06ReplayTestCase(unittest.TestCase):

    def ParseTestReplay(self, filename):
        with open(path.join('scores/replays_for_tests', filename), 'rb') as f:
            return replay_parsing.Parse(f.read())
    
    def testHard1cc(self):
        replay_info = self.ParseTestReplay('th6_hard_1cc.rpy')
        self.assertEqual(replay_info.game, 'th06')
        self.assertEqual(replay_info.difficulty, 2)
        self.assertEqual(replay_info.shot, 'ReimuA')
        self.assertEqual(replay_info.score, 92245410)

        # 6 stages (Hard 1cc)
        # Final score is 92245410
        # Final resources are 0 lives, 2 bombs

    def testExtra(self):
        replay_info = self.ParseTestReplay('th6_extra.rpy')
        self.assertEqual(replay_info.game, 'th06')
        self.assertEqual(replay_info.difficulty, 4)
        self.assertEqual(replay_info.shot, 'MarisaA')
        self.assertEqual(replay_info.score, 181144360)

class Th10ReplayTestCase(unittest.TestCase):
    
    def ParseTestReplay(self, filename):
        with open(path.join('scores/replays_for_tests', filename), 'rb') as f:
            return replay_parsing.Parse(f.read())
    
    def testNormal(self):
        rpy = self.ParseTestReplay('th10_normal.rpy')
        self.assertEqual(rpy.game, 'th10')
        self.assertEqual(rpy.difficulty, 1)
        self.assertEqual(rpy.shot, 'ReimuB')
        self.assertEqual(rpy.score, 294127890)
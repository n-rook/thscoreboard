import unittest
import replays.spell_cards as spell_cards

from replays.game_ids import GameIDs

class SpellNameTest(unittest.TestCase):
    def testEn(self):
        self.assertEqual(spell_cards.get_spell_name('en', GameIDs.TH08, 220, 7), '"Saigyouji Parinirvana"')
        self.assertEqual(spell_cards.get_spell_name('en', GameIDs.TH08, 221, 7), '"Profound Danmaku Barrier -Phantasm, Foam, and Shadow-"')
        self.assertEqual(spell_cards.get_spell_name('en', GameIDs.TH08, 222, 0), None)
        self.assertEqual(spell_cards.get_spell_name('en', GameIDs.TH08, 5, 3), 'Lamp Sign "Firefly Phenomenon"')
        self.assertEqual(spell_cards.get_spell_name('en', GameIDs.TH08, 48, 1), 'Ending Sign "Phantasmal Emperor"')


    def testJp(self):
        self.assertEqual(spell_cards.get_spell_name('jp', GameIDs.TH08, 220, 7), '「西行寺無余涅槃」')
        self.assertEqual(spell_cards.get_spell_name('jp', GameIDs.TH08, 221, 7), '「深弾幕結界　-夢幻泡影-」')
        self.assertEqual(spell_cards.get_spell_name('jp', GameIDs.TH08, 222, 0), None)
        self.assertEqual(spell_cards.get_spell_name('jp', GameIDs.TH08, 5, 3), '灯符「ファイヤフライフェノメノン」')
        self.assertEqual(spell_cards.get_spell_name('jp', GameIDs.TH08, 48, 1), '終符「幻想天皇」')

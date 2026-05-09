from django import test
from django.utils import translation
from django.conf import settings

from replays import spell_names


class SpellNamesTestCase(test.SimpleTestCase):
    def testSpellNameDictIntegrity(self):
        spell_names_en = spell_names.spell_names_en
        spell_names_jp = spell_names.spell_names_jp

        self.assertCountEqual(spell_names_en.keys(), spell_names_jp.keys())
        for game_id in spell_names_en:
            with self.subTest(game_id=game_id):
                self.assertEqual(
                    len(spell_names_en[game_id]),
                    len(spell_names_jp[game_id]),
                )

    def testSceneGameSpellNameDictIntegrity(self):
        language_codes = {code for code, _name in settings.LANGUAGES}
        for levels in spell_names.scene_game_spell_names.values():
            for level, scenes in levels.items():
                with self.subTest(level=level):
                    self.assertIsInstance(level, int)
                for scene, names in scenes.items():
                    with self.subTest(level=level, scene=scene):
                        self.assertIsInstance(scene, int)
                        self.assertEqual(set(names.keys()), language_codes)

    def testGetReturnsEnglishSpellName(self):
        with translation.override("en-us"):
            spell_name = spell_names.get(
                game_id="th08",
                spell_id=0,
                scene_game_level=None,
                scene_game_scene=None,
            )
        self.assertEqual('Firefly Sign "Earthly Meteor"', spell_name)

    def testGetReturnsJapaneseSpellName(self):
        with translation.override("ja"):
            spell_name = spell_names.get(
                game_id="th08",
                spell_id=0,
                scene_game_level=None,
                scene_game_scene=None,
            )
        self.assertEqual("蛍符「地上の流星」", spell_name)

    def testGetReturnsEnglishSceneGameSpellName(self):
        with translation.override("en-us"):
            spell_name = spell_names.get(
                game_id="th095",
                spell_id=None,
                scene_game_level=1,
                scene_game_scene=3,
            )
        self.assertEqual('Firefly Sign "Fixed Stars on Earth"', spell_name)

    def testGetReturnsJapaneseSceneGameSpellName(self):
        with translation.override("ja"):
            spell_name = spell_names.get(
                game_id="th095",
                spell_id=None,
                scene_game_level=1,
                scene_game_scene=3,
            )
        self.assertEqual("蛍符「地上の恒星」", spell_name)

    def testGetReturnsNoneForEnglishNonSpellPracticeMode(self):
        with translation.override("en-us"):
            spell_name = spell_names.get(
                game_id="th08",
                spell_id=None,
                scene_game_level=None,
                scene_game_scene=None,
            )
        self.assertIsNone(spell_name)

    def testGetReturnsNoneForJapaneseNonSpellPracticeMode(self):
        with translation.override("ja"):
            spell_name = spell_names.get(
                game_id="th08",
                spell_id=None,
                scene_game_level=None,
                scene_game_scene=None,
            )
        self.assertIsNone(spell_name)

    def testGetReturnsNoneForGameWithoutSpellPracticeNamesInEnglish(self):
        with translation.override("en-us"):
            spell_name = spell_names.get(
                game_id="th07",
                spell_id=None,
                scene_game_level=None,
                scene_game_scene=None,
            )
        self.assertIsNone(spell_name)

    def testGetReturnsNoneForGameWithoutSpellPracticeNamesInJapanese(self):
        with translation.override("ja"):
            spell_name = spell_names.get(
                game_id="th07",
                spell_id=None,
                scene_game_level=None,
                scene_game_scene=None,
            )
        self.assertIsNone(spell_name)

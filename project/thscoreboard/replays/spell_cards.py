from replays import game_ids
from immutabledict import immutabledict

import json
import logging


has_spell_practice = [game_ids.GameIDs.TH08]
thcrap_langs = ['en']


def _ReadSpellNames():
    spell_names = dict()
    for lang in thcrap_langs:
        spell_names[lang] = dict()
        for game_id in has_spell_practice:
            try:
                with open(f'replays/spells/{lang}/{game_id}.json', 'rb') as f:
                    spell_names[lang][game_id] = json.loads(f.read())
                    logging.info(f'replays/spells/{lang}/{game_id}.json loaded!')
            except FileNotFoundError:
                logging.error(f'replays/spells/{lang}/{game_id}.json not found!')
    return spell_names


_SPELL_NAMES = immutabledict(_ReadSpellNames())


def get_spell_name(lang: str, game_id: str, spell_id: int, difficulty: int = 0):
    """Retrieves a spell card's name based on a language, the gameid of the game it's from, a 0 indexed spell ID, and a difficulty ID"""
    for i in range(difficulty + 1):
        try:
            return _SPELL_NAMES[lang][game_id][f'{spell_id - i}']
        except KeyError:
            pass
    return None

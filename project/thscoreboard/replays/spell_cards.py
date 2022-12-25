from replays import game_ids
from immutabledict import immutabledict

import json
import logging


has_spell_practice = [game_ids.GameIDs.TH08]
thcrap_langs = ['en', 'jp']


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
    """Retrieves a spell card's name.
    
    Args:
      lang: A language code for the name.
      game_id: The game the spell card came from.
      spell_id: The spell card's ID (0-indexed).
      difficulty: The difficulty for the game.
    """
    for i in range(difficulty + 1):
        try:
            return _SPELL_NAMES[lang][game_id][f'{spell_id - i}']
        except KeyError:
            pass
    return None

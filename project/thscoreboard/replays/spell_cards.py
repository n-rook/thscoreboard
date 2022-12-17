from replays import game_ids

import json

spell_names = dict()
has_thcrap = [game_ids.GameIDs.TH06, game_ids.GameIDs.TH07, game_ids.GameIDs.TH08, game_ids.GameIDs.TH09, game_ids.GameIDs.TH10, game_ids.GameIDs.TH11]
thcrap_langs = ['en']
for lang in thcrap_langs:
    spell_names[lang] = dict()
    for game_id in has_thcrap:
        try:
            with open(f'replays/spells/{lang}/{game_id}.json', 'rb') as f:
                spell_names[lang][game_id] = json.loads(f.read())
        except FileNotFoundError:
            pass


def get_spell_name(lang, game_id, spell_id, difficulty):
    try:
        return spell_names[lang][game_id][f'{spell_id}']
    except KeyError:
        try:
            return spell_names[lang][game_id][f'{spell_id - difficulty}']
        except KeyError:
            return None

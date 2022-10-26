"""A class that provides methods used to properly format and display replay data"""

from immutabledict import immutabledict
from . import game_ids

_table_fields_th06 = immutabledict({
    'stage': True,
    'score': True,
    'piv': False,
    'graze': False,
    'point_items': False,
    'power': True,
    'lives': True,
    'life_pieces': False,
    'bombs': True,
    'bomb_pieces': False,
    'th06_rank': True,
    'th07_cherry': False,
    'th07_cherrymax': False
})

_table_fields_th07 = immutabledict({
    'stage': True,
    'score': True,
    'piv': True,
    'graze': True,
    'point_items': True,
    'power': True,
    'lives': True,
    'life_pieces': False,
    'bombs': True,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': True,
    'th07_cherrymax': True
})

_table_fields_th10 = immutabledict({
    'stage': True,
    'score': True,
    'piv': True,
    'graze': False,
    'point_items': False,
    'power': True,
    'lives': True,
    'life_pieces': False,
    'bombs': False,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False
})

_game_fields = immutabledict({
    'th01': None,
    'th05': None,
    'th06': _table_fields_th06,
    'th07': _table_fields_th07,
    'th10': _table_fields_th10
})


def GetPower(game_id: str, power: int):
    if game_id == game_ids.GameIDs.TH06:
        return power
    if game_id == game_ids.GameIDs.TH07:
        return power
    if game_id == game_ids.GameIDs.TH10:
        return "%.2f" % (float(power) * 0.05)

    return power


def GetGameField(gameid: str):
    if gameid in _game_fields:
        return _game_fields[gameid]
    return None

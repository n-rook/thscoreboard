"""A class that provides methods used to properly format and display replay data"""

import copy
from immutabledict import immutabledict
from typing import Optional
from . import game_ids

#   These table fields configure the display of the stage split columns
#   These may differ from whether the replay file actually has the field or not
#       depending on whether it is relevant to show that field
#   eg. life_pieces will almost always be False as displaying it is integrated into Lives

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
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
    'th13_trance': False,
    'extends': False,
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
    'th07_cherrymax': True,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
    'th13_trance': False,
    'extends': False,
})

_table_fields_th08 = immutabledict({
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
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
    'th13_trance': False,
    'extends': False,
})

_table_fields_th09 = immutabledict({
    'stage': True,
    'score': True,
    'piv': False,
    'graze': False,
    'point_items': False,
    'power': False,
    'lives': True,
    'life_pieces': False,
    'bombs': False,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': True,
    'th09_p2_score': True,
    'th13_trance': False,
    'extends': False,
})

_table_fields_th09_PVP = immutabledict({
    'stage': True,
    'score': False,
    'piv': False,
    'graze': False,
    'point_items': False,
    'power': False,
    'lives': False,
    'life_pieces': False,
    'bombs': False,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': True,
    'th09_p2_cpu': True,
    'th09_p2_shot': True,
    'th09_p2_score': False,
    'th13_trance': False,
    'extends': False,
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
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
    'th13_trance': False,
    'extends': False,
})

_table_fields_th11 = immutabledict({
    'stage': True,
    'score': True,
    'piv': True,
    'graze': True,
    'point_items': False,
    'power': True,
    'lives': True,
    'life_pieces': False,
    'bombs': False,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
    'th13_trance': False,
    'extends': False,
})

_table_fields_th12 = immutabledict({
    'stage': True,
    'score': True,
    'piv': True,
    'graze': True,
    'point_items': False,
    'power': True,
    'lives': True,
    'life_pieces': False,
    'bombs': True,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
    'th13_trance': False,
    'extends': False,
})

_table_fields_th13 = immutabledict({
    'stage': True,
    'score': True,
    'piv': True,
    'graze': True,
    'point_items': False,
    'power': True,
    'lives': True,
    'life_pieces': True,
    'bombs': True,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
    'th13_trance': True,
    'extends': True,
})

_table_fields_th14 = immutabledict({
    'stage': True,
    'score': True,
    'piv': True,
    'graze': True,
    'point_items': False,
    'power': True,
    'lives': True,
    'life_pieces': False,
    'bombs': True,
    'bomb_pieces': True,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
    'th13_trance': False,
    'extends': False,
})

_table_fields_th15 = immutabledict({
    'stage': True,
    'score': True,
    'piv': True,
    'graze': True,
    'point_items': False,
    'power': True,
    'lives': True,
    'life_pieces': False,
    'bombs': True,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
    'th13_trance': False,
    'extends': False,
})

_table_fields_th16 = immutabledict({
    'stage': True,
    'score': True,
    'piv': True,
    'graze': True,
    'point_items': False,
    'power': True,
    'lives': True,
    'life_pieces': False,
    'bombs': True,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
    'th13_trance': False,
    'extends': False,
})

_table_fields_th17 = immutabledict({
    'stage': True,
    'score': True,
    'piv': True,
    'graze': True,
    'point_items': False,
    'power': True,
    'lives': True,
    'life_pieces': False,
    'bombs': True,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
    'th13_trance': False,
    'extends': False,
})

_table_fields_th18 = immutabledict({
    'stage': True,
    'score': True,
    'piv': True,
    'graze': True,
    'point_items': False,
    'power': True,
    'lives': True,
    'life_pieces': False,
    'bombs': True,
    'bomb_pieces': False,
    'th06_rank': False,
    'th07_cherry': False,
    'th07_cherrymax': False,
    'th09_p1_cpu': False,
    'th09_p2_cpu': False,
    'th09_p2_shot': False,
    'th09_p2_score': False,
    'th13_trance': False,
    'extends': False,
})

_game_fields = immutabledict({
    'th01': None,
    'th05': None,
    'th06': _table_fields_th06,
    'th07': _table_fields_th07,
    'th08': _table_fields_th08,
    'th09': _table_fields_th09,
    'th10': _table_fields_th10,
    'th11': _table_fields_th11,
    'th12': _table_fields_th12,
    'th13': _table_fields_th13,
    'th14': _table_fields_th14,
    'th15': _table_fields_th15,
    'th16': _table_fields_th16,
    'th17': _table_fields_th17,
    'th18': _table_fields_th18,
})

_game_fields_PVP = immutabledict({
    'th01': None,
    'th05': None,
    'th06': None,
    'th07': None,
    'th08': None,
    'th09': _table_fields_th09_PVP,
    'th10': None,
    'th11': None,
    'th12': None,
    'th13': None,
    'th14': None,
    'th15': None,
    'th16': None,
    'th17': None,
    'th18': None,
})


def GetFormatPower(game_id: str, power: Optional[int]) -> str:
    if power is None:
        return ""
    if game_id in (game_ids.GameIDs.TH06, game_ids.GameIDs.TH07, game_ids.GameIDs.TH08):
        return str(power)
    if game_id in (game_ids.GameIDs.TH10, game_ids.GameIDs.TH11):
        return "%.2f" % (float(power) * 0.05)
    if game_id in (
        game_ids.GameIDs.TH12,
        game_ids.GameIDs.TH13,
        game_ids.GameIDs.TH14,
        game_ids.GameIDs.TH15,
        game_ids.GameIDs.TH16,
        game_ids.GameIDs.TH17,
        game_ids.GameIDs.TH18,
    ):
        return '{:.2f}'.format(power / 100)

    return str(power)


# used in GetFormatLives for string formatting the life/life piece counts
# if this is None, lives will be displayed standalone instead of including the life piece counts
_life_pieces = immutabledict({
    'th01': None,
    'th02': None,
    'th03': None,
    'th04': None,
    'th05': None,
    'th06': None,
    'th07': None,
    'th08': None,
    'th09': None,
    'th10': None,
    'th11': 5,
    'th12': 4,
    'th13': None,   # this game has variable life pieces, so hardcoding it doesn't work
    'th14': 3,
    'th15': 3,
    'th16': None,
    'th17': 3,
    'th18': 3,
})


# used in GetFormatBombs for string formatting the bomb/bomb piece counts
_bomb_pieces = immutabledict({
    'th01': None,
    'th02': None,
    'th03': None,
    'th04': None,
    'th05': None,
    'th06': None,
    'th07': None,
    'th08': None,
    'th09': None,
    'th10': None,
    'th11': None,
    'th12': 3,
    'th13': 8,
    'th14': 8,
    'th15': 5,
    'th16': 5,
    'th17': 3,
    'th18': 3,
})


def GetFormatLives(game_id: str, lives: Optional[int], life_pieces: Optional[int]) -> str:
    if lives is None:
        return ""
    total_life_pieces = _life_pieces[game_id]
    if total_life_pieces is None:
        return str(lives)
    else:
        if life_pieces is None:
            life_pieces = 0
        return f"{lives} ({life_pieces}/{total_life_pieces})"


def GetFormatBombs(game_id: str, bombs: Optional[int], bomb_pieces: Optional[int]) -> str:
    if bombs is None:
        return ""
    total_bomb_pieces = _bomb_pieces[game_id]
    if total_bomb_pieces is None:
        return str(bombs)
    else:
        if bomb_pieces is None:
            bomb_pieces = 0
        return f"{bombs} ({bomb_pieces}/{total_bomb_pieces})"


def GetGameField(gameid: str, replay_type: game_ids.ReplayTypes):
    if replay_type is game_ids.ReplayTypes.PVP:
        if gameid in _game_fields_PVP:
            return _game_fields_PVP[gameid]
    else:
        if gameid in _game_fields:
            return _game_fields[gameid]
    return None


def GetGameLifePieces(gameid: str):
    if gameid in _life_pieces:
        return _life_pieces[gameid]
    return None


FORMAT_EXTRA = 'Extra'
FORMAT_PHANTASM = 'Phantasm'


def GetFormatStage(game_id: str, stage: Optional[int]) -> str:
    if stage is None:
        return ''
    if game_id == "th08":
        stages = {
            1: '1',
            2: '2',
            3: '3',
            4: '4A',
            5: '4B',
            6: '5',
            7: '6A',
            8: '6B',
            9: FORMAT_EXTRA,
        }
        return stages[stage]
    if game_id == 'th09':
        if stage == 10:
            return FORMAT_EXTRA
    elif game_id == 'th07' and stage == 8:
        return FORMAT_PHANTASM
    elif stage == 7:
        return FORMAT_EXTRA
    return str(stage)


def GetFormatLifePieces(game_id: str, life_pieces: Optional[int], extends: Optional[int] = 0) -> str:
    if life_pieces is None:
        return ""
    if extends is None:
        return str(life_pieces)
    if game_id == 'th13':
        threshholds = [8, 10, 12, 15, 18, 20, 25]
        if extends > 5:
            extends = 6
        return f'{life_pieces}/{threshholds[extends]}'
    else:
        return str(life_pieces)


def FormatStages(game_id: str, replay_stages):
    """This function formats the stage values to be displayed in the front end"""
    new_stages = copy.deepcopy(replay_stages)

    for stage in new_stages:
        stage.power = GetFormatPower(game_id, stage.power)
        stage.stage = GetFormatStage(game_id, stage.stage)
        stage.lives = GetFormatLives(game_id, stage.lives, stage.life_pieces)
        stage.bombs = GetFormatBombs(game_id, stage.bombs, stage.bomb_pieces)
        stage.life_pieces = GetFormatLifePieces(game_id, stage.life_pieces, stage.extends)
        if game_id == game_ids.GameIDs.TH09:
            stage.th09_p2_shotFormat = stage.th09_p2_shot.GetName()

        if stage.stage is None:
            stage.stage = ""
        if stage.score is None:
            stage.score = ""
        if stage.piv is None:
            stage.piv = ""
        if stage.graze is None:
            stage.graze = ""
        if stage.point_items is None:
            stage.point_items = ""
        if stage.power is None:
            stage.power = ""
        if stage.lives is None:
            stage.lives = ""
        if stage.life_pieces is None:
            stage.life_pieces = ""
        if stage.bombs is None:
            stage.bombs = ""
        if stage.bomb_pieces is None:
            stage.bomb_pieces = ""
        if stage.th06_rank is None:
            stage.th06_rank = ""
        if stage.th07_cherry is None:
            stage.th07_cherry = ""
        if stage.th07_cherrymax is None:
            stage.th07_cherrymax = ""
        if stage.th09_p1_cpu is None:
            stage.th09_p1_cpu = ""
        if stage.th09_p2_cpu is None:
            stage.th09_p2_cpu = ""
        if stage.th09_p2_score is None:
            stage.th09_p2_score = ""
        if stage.th13_trance is None:
            stage.th13_trance = ""
        if stage.extends is None:
            stage.extends = ""

    return new_stages
